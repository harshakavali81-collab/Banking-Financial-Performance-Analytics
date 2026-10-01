"""Reproducible synthetic banking analytics. Run: python src/pipeline.py"""
from pathlib import Path
import json, sqlite3, calendar, argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
MONTHS = pd.date_range('2025-01-31', '2025-12-31', freq='ME')
SEED = 81

def save(frame, folder, name):
    frame.to_csv(ROOT / folder / f'{name}.csv', index=False)

def generate():
    rng = np.random.default_rng(SEED)
    branches = pd.DataFrame({'branch_id':range(1,9),
        'branch_name':['Hyderabad Central','Hyderabad West','Bengaluru Central','Bengaluru East','Chennai Central','Pune Central','Mumbai Central','Delhi Central'],
        'city':['Hyderabad','Hyderabad','Bengaluru','Bengaluru','Chennai','Pune','Mumbai','Delhi'],
        'region':['South','South','South','South','South','West','West','North']})
    n=2500
    customers=pd.DataFrame({'customer_id':range(1,n+1),'customer_name':[f'Demo Customer {i:04}' for i in range(1,n+1)],
        'age':rng.integers(21,71,n),'occupation':rng.choice(['Salaried','Self-employed','Student','Retired'],n,p=[.55,.3,.05,.1]),
        'annual_income':np.round(rng.lognormal(13.25,.55,n),2),'credit_score':np.clip(rng.normal(710,75,n),300,900).astype(int),
        'home_branch_id':rng.integers(1,9,n)})
    na=3200
    owners=np.concatenate([np.arange(1,n+1),rng.integers(1,n+1,na-n)])
    accounts=pd.DataFrame({'account_id':range(1,na+1),'customer_id':owners,
        'branch_id':customers.set_index('customer_id').loc[owners,'home_branch_id'].values,
        'account_type':rng.choice(['Savings','Current'],na,p=[.8,.2]),
        'open_date':['2024-01-01']*na,'opening_balance':np.round(rng.lognormal(11.8,.65,na),2)})
    nt=40000
    aid=rng.integers(1,na+1,nt)
    dates=pd.Timestamp('2025-01-01')+pd.to_timedelta(rng.integers(0,365,nt),unit='D')
    kinds=rng.choice(['Deposit','Withdrawal','Transfer In','Transfer Out','Card Payment'],nt,p=[.34,.2,.15,.11,.2])
    amounts=np.round(rng.lognormal(8.4,.9,nt),2)
    transactions=pd.DataFrame({'transaction_id':range(1,nt+1),'account_id':aid,'transaction_date':dates.strftime('%Y-%m-%d'),
        'transaction_type':kinds,'amount':amounts,'channel':rng.choice(['Mobile','Internet','ATM','Branch'],nt,p=[.45,.27,.18,.1])})
    transactions=transactions.sort_values(['transaction_date','transaction_id']).reset_index(drop=True)
    balances=accounts.set_index('account_id').opening_balance.to_dict()
    for idx,row in transactions.iterrows():
        sign=1 if row.transaction_type in ['Deposit','Transfer In'] else -1
        if sign<0 and balances[row.account_id]<row.amount:
            transactions.loc[idx,'transaction_type']='Deposit'
            sign=1
        balances[row.account_id]=round(balances[row.account_id]+sign*row.amount,2)
    delta=transactions.amount*np.where(transactions.transaction_type.isin(['Deposit','Transfer In']),1,-1)
    monthly_delta=transactions.assign(month=transactions.transaction_date.str[:7],delta=delta).pivot_table(index='account_id',columns='month',values='delta',aggfunc='sum',fill_value=0)
    running=accounts.opening_balance.to_numpy().copy()
    account_snapshots=[]
    for month in MONTHS:
        running=np.round(running+monthly_delta.reindex(accounts.account_id,fill_value=0)[month.strftime('%Y-%m')].values,2)
        account_snapshots.append(pd.DataFrame({'snapshot_date':month.strftime('%Y-%m-%d'),'account_id':accounts.account_id,'balance':running}))
    account_snapshots=pd.concat(account_snapshots,ignore_index=True)
    nl=1200
    loan_customer=rng.choice(customers.customer_id,nl,replace=False)
    loans=pd.DataFrame({'loan_id':range(1,nl+1),'customer_id':loan_customer,
        'branch_id':customers.set_index('customer_id').loc[loan_customer,'home_branch_id'].values,
        'loan_type':rng.choice(['Home','Personal','Auto','Education','Business'],nl,p=[.25,.35,.2,.08,.12]),
        'origination_date':['2024-12-15']*nl,
        'original_principal':np.round(rng.lognormal(13.6,.7,nl),2),
        'annual_interest_rate':np.round(rng.uniform(.08,.18,nl),4),
        'tenure_months':rng.choice([24,36,60,120],nl)})
    repayments=[]; loan_snapshots=[]; pid=0
    for row in loans.itertuples(index=False):
        score=customers.loc[customers.customer_id==row.customer_id,'credit_score'].iloc[0]
        missed_probability=float(np.clip((790-score)/2500+.015,.01,.2))
        balance=row.original_principal; oldest_unpaid=None
        for month in MONTHS:
            due=pd.Timestamp(month.year,month.month,5)
            principal=round(min(row.original_principal/row.tenure_months,balance),2)
            interest=round(balance*row.annual_interest_rate/12,2)
            paid=bool(rng.random()>missed_probability)
            pid+=1
            if not paid and oldest_unpaid is None: oldest_unpaid=due
            payment_date=(due+pd.Timedelta(days=int(rng.integers(0,6)))).strftime('%Y-%m-%d') if paid else None
            repayments.append([pid,row.loan_id,due.strftime('%Y-%m-%d'),payment_date,principal,interest,principal if paid else 0,interest if paid else 0,'Paid' if paid else 'Unpaid'])
            balance=round(balance-(principal if paid else 0),2)
            dpd=(month-oldest_unpaid).days if oldest_unpaid is not None else 0
            loan_snapshots.append([month.strftime('%Y-%m-%d'),row.loan_id,balance,dpd])
    repayments=pd.DataFrame(repayments,columns=['payment_id','loan_id','due_date','payment_date','principal_due','interest_due','principal_paid','interest_paid','payment_status'])
    loan_snapshots=pd.DataFrame(loan_snapshots,columns=['snapshot_date','loan_id','outstanding','days_past_due'])
    # Deliberate raw-data defects. Exact duplicates and recognized aliases are repairable;
    # ambiguous invalid facts are quarantined rather than imputed.
    rawtx=transactions.copy()
    rawtx.loc[:39,'channel']=' mobile '
    rawtx=pd.concat([rawtx,rawtx.iloc[:100]],ignore_index=True)
    bad=transactions.iloc[:15].copy()
    bad.transaction_id=np.arange(40001,40016)
    bad.loc[bad.index[:5],'amount']=-100
    bad.loc[bad.index[5:10],'account_id']=999999
    bad.loc[bad.index[10:],'transaction_date']='bad-date'
    rawtx=pd.concat([rawtx,bad],ignore_index=True)
    rawcust=customers.copy(); rawcust.loc[:19,'occupation']=None
    frames={'branches':branches,'customers':rawcust,'accounts':accounts,'transactions':rawtx,'loans':loans,
        'repayments':repayments,'account_snapshots':account_snapshots,'loan_snapshots':loan_snapshots}
    for name,frame in frames.items(): save(frame,'data/raw',name)

def clean():
    names=['branches','customers','accounts','transactions','loans','repayments','account_snapshots','loan_snapshots']
    data={name:pd.read_csv(ROOT/'data/raw'/f'{name}.csv') for name in names}
    t=data['transactions']; raw_n=len(t)
    t=t.drop_duplicates().copy()
    removed=raw_n-len(t)
    t['channel']=t.channel.str.strip().str.title()
    t['transaction_date']=pd.to_datetime(t.transaction_date,errors='coerce')
    t['amount']=pd.to_numeric(t.amount,errors='coerce')
    valid=t.amount.gt(0)&t.account_id.isin(data['accounts'].account_id)&t.transaction_date.notna()
    rejected=t.loc[~valid].copy()
    rejected['reason']=np.select([rejected.amount.le(0),~rejected.account_id.isin(data['accounts'].account_id),rejected.transaction_date.isna()],['non-positive amount','unknown account','invalid date'],default='invalid amount')
    save(rejected,'data/quarantine','transactions')
    t=t.loc[valid].copy(); t.transaction_date=t.transaction_date.dt.strftime('%Y-%m-%d')
    t['signed_amount']=t.amount*np.where(t.transaction_type.isin(['Deposit','Transfer In']),1,-1)
    t=t.merge(data['accounts'][['account_id','customer_id','branch_id']],on='account_id',validate='many_to_one')
    data['transactions']=t
    missing=int(data['customers'].occupation.isna().sum())
    data['customers']['occupation']=data['customers'].occupation.fillna('Unknown')
    for name,frame in data.items(): save(frame,'data/clean',name)
    audit={'raw_transactions':raw_n,'exact_duplicates_removed':removed,'transactions_quarantined':len(rejected),
        'clean_transactions':len(t),'channel_aliases_normalized':40,'missing_occupations_labelled_unknown':missing}
    (ROOT/'outputs/cleaning_audit.json').write_text(json.dumps(audit,indent=2))
    return data,audit

def build_financials(data):
    loans=data['loans']; reps=data['repayments'].merge(loans[['loan_id','branch_id']],on='loan_id',validate='many_to_one')
    ac=data['account_snapshots'].merge(data['accounts'][['account_id','branch_id','account_type']],on='account_id',validate='many_to_one')
    ls=data['loan_snapshots'].merge(loans[['loan_id','branch_id']],on='loan_id',validate='many_to_one')
    out=[]
    opening=data['accounts'].groupby('branch_id').opening_balance.sum().to_dict()
    for month in MONTHS:
        date=month.strftime('%Y-%m-%d'); key=month.strftime('%Y-%m')
        for bid in data['branches'].branch_id:
            a=ac[(ac.snapshot_date==date)&(ac.branch_id==bid)]
            closing=a.balance.sum(); avg=(opening[bid]+closing)/2
            l=ls[(ls.snapshot_date==date)&(ls.branch_id==bid)].outstanding.sum()
            r=reps[(reps.due_date.str[:7]==key)&(reps.branch_id==bid)]
            income=round(r.interest_paid.sum(),2)
            funding=round(max(l-closing,0)*.08/12,2)
            expense=round(avg*.035/12+funding,2)
            tx=data['transactions']; selected=tx[(tx.transaction_date.str[:7]==key)&(tx.branch_id==bid)]
            fees=round(len(selected)*18,2)
            opex=round(70000+len(a)*75+len(selected)*9,2)
            out.append([date,bid,income,expense,fees,opex])
            opening[bid]=closing
    data['branch_financials']=pd.DataFrame(out,columns=['snapshot_date','branch_id','interest_income','interest_expense','fee_income','operating_expense'])
    save(data['branch_financials'],'data/clean','branch_financials')
    return data

def database(data):
    dbpath=ROOT/'outputs/banking.db'
    dbpath.unlink(missing_ok=True)
    con=sqlite3.connect(dbpath)
    con.executescript((ROOT/'sql/schema.sql').read_text())
    for name,frame in data.items(): frame.to_sql(name,con,index=False,if_exists='append')
    assert not con.execute('PRAGMA foreign_key_check').fetchall()
    for block in (ROOT/'sql/analysis.sql').read_text().split('-- QUERY: ')[1:]:
        name,query=block.split('\n',1)
        result=pd.read_sql_query(query,con)
        save(result,'outputs/sql_results',name.strip())
    return con

def analyze(data,con,audit):
    latest='2025-12-31'
    accounts=data['account_snapshots'].query('snapshot_date == @latest')
    loans=data['loan_snapshots'].query('snapshot_date == @latest')
    fin=data['branch_financials']; tx=data['transactions']
    dep=float(accounts.balance.sum()); outstanding=float(loans.outstanding.sum())
    income=float(fin.interest_income.sum()); expense=float(fin.interest_expense.sum()); fees=float(fin.fee_income.sum()); opex=float(fin.operating_expense.sum())
    overdue=loans.days_past_due.ge(90)
    k={'customers':len(data['customers']),'accounts':len(data['accounts']),'loans':len(data['loans']),
        'deposit_balance':round(dep,2),'loan_outstanding':round(outstanding,2),
        'loan_to_deposit_ratio':outstanding/dep,'dpd90_exposure_ratio':float(loans.loc[overdue,'outstanding'].sum()/outstanding),
        'dpd90_loan_rate':float(overdue.mean()),'transaction_count':len(tx),'transaction_value':round(float(tx.amount.sum()),2),
        'digital_share':float(tx.channel.isin(['Mobile','Internet']).mean()),'interest_income':round(income,2),
        'interest_expense':round(expense,2),'net_interest_income':round(income-expense,2),'fee_income':round(fees,2),
        'operating_expense':round(opex,2),'operating_profit':round(income-expense+fees-opex,2),
        'cost_to_income_ratio':opex/(income-expense+fees),
        'deposit_growth':dep/float(data['accounts'].opening_balance.sum())-1}
    (ROOT/'outputs/kpis.json').write_text(json.dumps(k,indent=2))
    branch=pd.read_csv(ROOT/'outputs/sql_results/branch_performance.csv')
    monthly=pd.read_csv(ROOT/'outputs/sql_results/monthly_performance.csv')
    risk=pd.read_csv(ROOT/'outputs/sql_results/risk_by_score.csv')
    channels=pd.read_csv(ROOT/'outputs/sql_results/channel_mix.csv')
    # Independent business reconciliations catch snapshot double counting and join fan-out.
    checks={
        'transaction_count':len(tx)==40000,
        'raw_rows_accounted':audit['raw_transactions']==audit['clean_transactions']+audit['exact_duplicates_removed']+audit['transactions_quarantined'],
        'account_ledger_reconciles':bool(np.isclose(dep,data['accounts'].opening_balance.sum()+tx.signed_amount.sum(),atol=.01)),
        'loan_principal_reconciles':bool(np.isclose(outstanding,data['loans'].original_principal.sum()-data['repayments'].principal_paid.sum(),atol=.01)),
        'branch_deposits_reconcile':bool(np.isclose(dep,branch.deposit_balance.sum(),atol=.01)),
        'branch_profit_reconciles':bool(np.isclose(k['operating_profit'],branch.operating_profit.sum(),atol=.01)),
        'nonnegative_account_balances':bool(data['account_snapshots'].balance.ge(0).all()),
        'foreign_keys_valid':not bool(con.execute('PRAGMA foreign_key_check').fetchall()),
        'dpd_bounds':bool(data['loan_snapshots'].days_past_due.between(0,365).all())}
    assert all(checks.values()),checks
    (ROOT/'outputs/validation.json').write_text(json.dumps(checks,indent=2))
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':'#475569'})
    fig,axs=plt.subplots(2,2,figsize=(14,8.5)); fig.patch.set_facecolor('#f8fafc')
    fig.suptitle('BANKING PERFORMANCE | Synthetic 2025 portfolio',fontsize=18,x=.06,ha='left',color='#0f172a')
    axs[0,0].plot(monthly.month.str[5:],monthly.deposit_balance/1e7,color='#2563eb',marker='o',label='Deposits')
    axs[0,0].plot(monthly.month.str[5:],monthly.loan_outstanding/1e7,color='#0d9488',marker='o',label='Loans')
    axs[0,0].set(title='Month-end balances',ylabel='INR crore',xlabel='Month'); axs[0,0].legend()
    axs[0,1].barh(branch.branch_name,branch.deposit_balance/1e7,color='#2563eb'); axs[0,1].set(title='Branch deposits at 31 Dec',xlabel='INR crore')
    axs[1,0].bar(risk.score_band,risk.dpd90_loan_rate*100,color='#e89d3c'); axs[1,0].set(title='90+ DPD loan rate by credit score',ylabel='% of loans at 31 Dec',xlabel='Credit score band')
    axs[1,1].bar(channels.channel,channels.transaction_count,color='#0d9488'); axs[1,1].set(title='Annual transaction channels',ylabel='Transactions')
    fig.tight_layout(rect=[0,0,1,.93]); fig.savefig(ROOT/'outputs/charts/dashboard.png',dpi=160); plt.close(fig)
    enriched=data['loans'].merge(data['customers'][['customer_id','annual_income','credit_score']],on='customer_id',validate='many_to_one')
    fig,axs=plt.subplots(1,2,figsize=(12,4)); axs[0].hist(data['customers'].credit_score,bins=24,color='#2563eb'); axs[0].set(title='Customer credit score distribution',xlabel='Credit score',ylabel='Customers')
    axs[1].scatter(enriched.annual_income/1e5,enriched.original_principal/1e5,s=9,alpha=.3,color='#0d9488'); axs[1].set(title='Income and original loan principal',xlabel='Annual income (INR lakh)',ylabel='Original principal (INR lakh)')
    fig.tight_layout(); fig.savefig(ROOT/'outputs/charts/customer_eda.png',dpi=160); plt.close(fig)
    return k,branch,monthly,risk,channels

def documents(k,branch,monthly,risk,channels,audit):
    top=branch.sort_values('deposit_balance',ascending=False).iloc[0]
    r=risk.sort_values('dpd90_loan_rate',ascending=False).iloc[0]
    insights=[f"{top.branch_name} has the largest deposit balance: INR {top.deposit_balance/1e7:.2f} crore, {top.deposit_balance/k['deposit_balance']:.1%} of the portfolio.",
        f"Deposits changed {k['deposit_growth']:.1%} from the 1 January opening balance to 31 December.",
        f"Mobile and Internet account for {k['digital_share']:.1%} of annual transactions.",
        f"The {r.score_band} score band has the highest 90+ DPD loan rate ({r.dpd90_loan_rate:.1%}, {int(r.loan_count)} loans). This pattern is partly programmed into the simulation.",
        f"90+ DPD balances represent {k['dpd90_exposure_ratio']:.1%} of outstanding loans. This is an analytical proxy, not a regulatory NPA classification.",
        f"Annual management operating profit before credit losses and tax is INR {k['operating_profit']/1e7:.2f} crore."]
    recommendations=['Prioritize a collections review of 90+ DPD loans, recording recoveries and arrears before interpreting risk trends.',
        'Review funding needs alongside the loan-to-deposit ratio. Wholesale funding expense is explicitly modeled for branches with a funding gap.',
        'Compare branch operating costs and income before reallocating resources. Test any proposed change against real operational constraints.',
        'Replace simulated patterns with appropriately anonymized real data before making a banking decision.']
    report='# Banking & Financial Performance Analytics\n\nSynthetic portfolio. Reporting year: 2025. Snapshot: 31 December 2025. Currency: INR.\n\n'
    report+='## Findings\n\n'+'\n'.join('- '+s for s in insights)+'\n\n## Recommendations\n\n'+'\n'.join('- '+s for s in recommendations)
    report+='\n\n## Data quality\n\n'+json.dumps(audit,indent=2)+'\n\n## Limits\n\nAll customers, transactions and results are generated with seed 81. The loan schedule uses equal principal installments, not fixed-EMI amortization. Missed installments remain unpaid through year-end; later scheduled payments do not clear older arrears. Interest income is cash received. Deposit cost uses average opening/closing monthly balances and a 3.5% annual rate. Wholesale funding uses an 8% annual rate for positive branch loan-minus-deposit gaps. Fees are separately simulated at INR 18 per transaction. Operating profit excludes credit-loss provisions and tax. Fee and deposit-interest postings are outside the customer transaction ledger. No financial prediction or regulatory compliance is claimed.\n'
    (ROOT/'docs/business_report.md').write_text(report)
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    font_path=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    font_name='Helvetica'; bold_name='Helvetica-Bold'
    if font_path.exists():
        pdfmetrics.registerFont(TTFont('ReportSans',str(font_path)))
        pdfmetrics.registerFont(TTFont('ReportSansBold',str(font_path.with_name('DejaVuSans-Bold.ttf'))))
        font_name='ReportSans'; bold_name='ReportSansBold'
    styles=getSampleStyleSheet(); styles['Title'].textColor=colors.HexColor('#0f172a'); styles['Title'].alignment=TA_LEFT
    styles['BodyText'].fontSize=10; styles['BodyText'].leading=14
    for style in styles.byName.values(): style.fontName=bold_name if style.name in ['Title','Heading1','Heading2'] else font_name
    story=[Paragraph('Banking & Financial<br/>Performance Analytics',styles['Title']),Paragraph('Synthetic portfolio | 2025 | INR',styles['BodyText']),Spacer(1,16)]
    rows=[['Metric','Result'],['Customers',f"{k['customers']:,}"],['Deposit balance (31 Dec)',f"INR {k['deposit_balance']/1e7:.2f} crore"],['Loan outstanding (31 Dec)',f"INR {k['loan_outstanding']/1e7:.2f} crore"],['Loan-to-deposit ratio',f"{k['loan_to_deposit_ratio']:.1%}"],['90+ DPD exposure ratio (proxy)',f"{k['dpd90_exposure_ratio']:.1%}"],['Annual operating profit before losses/tax',f"INR {k['operating_profit']/1e7:.2f} crore"],['Clean annual transactions',f"{k['transaction_count']:,}"]]
    table=Table(rows,colWidths=[315,165]); table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#183557')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f1f5f9'),colors.white])]))
    table.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),font_name),('FONTNAME',(0,0),(-1,0),bold_name)]))
    story+=[table,Spacer(1,16),Paragraph('Findings',styles['Heading2'])]
    for s in insights: story.extend([Paragraph(s,styles['BodyText']),Spacer(1,7)])
    story+=[PageBreak(),Paragraph('Portfolio dashboard',styles['Heading1']),Image(str(ROOT/'outputs/charts/dashboard.png'),width=490,height=298),Spacer(1,12),Paragraph('Recommended next steps',styles['Heading2'])]
    for s in recommendations: story.extend([Paragraph(s,styles['BodyText']),Spacer(1,7)])
    story += [PageBreak(),Paragraph('Methodology and validation',styles['Heading1']),Paragraph('Data quality: '+', '.join(f'{a.replace("_"," ")}: {b}' for a,b in audit.items()),styles['BodyText']),Spacer(1,12),Image(str(ROOT/'outputs/charts/customer_eda.png'),width=490,height=163),Spacer(1,12)]
    for s in report.split('## Limits\n\n')[1].strip().split('. '): story.extend([Paragraph(s,styles['BodyText']),Spacer(1,5)])
    story+=[Spacer(1,8),Paragraph('All nine pipeline validation checks passed: transaction accounting, account and loan roll-forwards, branch deposit and profit reconciliation, non-negative balances, foreign keys and DPD bounds.',styles['BodyText'])]
    def footer(canvas,doc):
        canvas.setFont(font_name,8); canvas.setFillColor(colors.HexColor('#64748b')); canvas.drawString(48,28,'Kavali Harshavardhan | Synthetic banking analytics'); canvas.drawRightString(547,28,str(doc.page))
    SimpleDocTemplate(str(ROOT/'outputs/Banking_Analytics_Report.pdf'),leftMargin=48,rightMargin=48,topMargin=42,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
    payload={'kpis':k,'branches':branch.to_dict('records'),'monthly':monthly.to_dict('records'),'risk':risk.to_dict('records'),'channels':channels.to_dict('records'),'insights':insights}
    (ROOT/'outputs/dashboard_data.json').write_text(json.dumps(payload,indent=2))
    template=(ROOT/'src/dashboard_template.html').read_text()
    (ROOT/'outputs/Banking_Dashboard.html').write_text(template.replace('__DATA__',json.dumps(payload)))
    # Typed intermediates for workbook builder; full clean tables remain in CSV/database.
    sheets={'Monthly':monthly,'Branches':branch,'Risk':risk,'Channels':channels}
    (ROOT/'outputs/workbook_data.json').write_text(json.dumps({n:{'columns':list(df.columns),'rows':df.values.tolist()} for n,df in sheets.items()},indent=2))

def main():
    for folder in ['data/raw','data/clean','data/quarantine','outputs/sql_results','outputs/charts','docs']:(ROOT/folder).mkdir(parents=True,exist_ok=True)
    generate(); data,audit=clean(); data=build_financials(data); con=database(data)
    k,branch,monthly,risk,channels=analyze(data,con,audit); documents(k,branch,monthly,risk,channels,audit); con.close()
    print(json.dumps({'status':'passed','kpis':k,'cleaning':audit},indent=2))

if __name__=='__main__': main()
