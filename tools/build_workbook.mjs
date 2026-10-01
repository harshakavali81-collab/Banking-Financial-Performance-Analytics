import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('..',import.meta.url));
const data=JSON.parse(await fs.readFile(root+'/outputs/workbook_data.json','utf8'));
const k=JSON.parse(await fs.readFile(root+'/outputs/kpis.json','utf8'));
const wb=Workbook.create();const summary=wb.worksheets.add('Overview');
for(const name of Object.keys(data)) wb.worksheets.add(name);
for(const [name,obj] of Object.entries(data)){
 const s=wb.worksheets.getItem(name);s.showGridLines=false;
 const rows=obj.rows.map(row=>row.map((v,i)=>obj.columns[i]==='snapshot_date'?new Date(v+'T00:00:00Z'):v));
 s.getRange('A1').write([obj.columns,...rows]);
 s.getUsedRange().format.font={name:'Arial',size:10};s.getUsedRange().format.rowHeight=23;s.getUsedRange().format.columnWidth=19;
 s.getRangeByIndexes(0,0,1,obj.columns.length).format={fill:'#173a5e',font:{name:'Arial',size:10,bold:true,color:'#ffffff'},rowHeight:45,wrapText:true,horizontalAlignment:'center',verticalAlignment:'center'};
 s.getRangeByIndexes(1,0,rows.length,obj.columns.length).setNumberFormat('#,##0.00');
 for(let c=0;c<obj.columns.length;c++){
  const col=obj.columns[c];const r=s.getRangeByIndexes(1,c,rows.length,1);
  if(col==='snapshot_date')r.setNumberFormat('dd-mmm-yyyy');
  else if(typeof rows[0][c]==='string')r.setNumberFormat('@');
  else if(/ratio|rate|share/.test(col))r.setNumberFormat('0.0%');
  else if(/count|customers|branch_id/.test(col))r.setNumberFormat('#,##0');
 }
 s.freezePanes.freezeRows(1);
 s.tables.add(s.getUsedRange().address??`A1:${String.fromCharCode(64+obj.columns.length)}${rows.length+1}`,true,`${name}Data`);
 if(name==='Branches'){s.getRange('B:B').format.columnWidth=26;}
}
const m=wb.worksheets.getItem('Monthly');
// Monthly ledger owns the income calculations; source inputs remain editable.
m.getRange('J2:K13').formulas=Array.from({length:12},(_,i)=>[`=F${i+2}-G${i+2}`,`=J${i+2}+H${i+2}-I${i+2}`]);
const b=wb.worksheets.getItem('Branches');
b.getRange('I2:J9').formulas=Array.from({length:8},(_,i)=>[`=G${i+2}/E${i+2}`,`=H${i+2}/G${i+2}`]);
b.getRange('N2:N9').formulas=Array.from({length:8},(_,i)=>[`=K${i+2}+L${i+2}-M${i+2}`]);
summary.showGridLines=false;summary.tabColor='#173a5e';
summary.getRange('A1:L40').format.font={name:'Arial',size:10};summary.getRange('A1:L40').format.columnWidth=13;summary.getRange('A1:L40').format.rowHeight=24;
summary.getRange('A2').values=[['Banking performance analytics']];summary.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#173a5e'};
summary.getRange('A3').values=[['Synthetic 2025 portfolio. Stocks at 31 Dec; flows for the full year.']];summary.getRange('A3').format.font={italic:true,color:'#64748b'};
summary.getRange('A5:C5').values=[['Metric','Result','Basis']];summary.getRange('A5:C5').format={fill:'#173a5e',font:{bold:true,color:'#ffffff'},rowHeight:25};
summary.getRange('A:A').format.columnWidth=39;summary.getRange('B:B').format.columnWidth=21;summary.getRange('C:C').format.columnWidth=30;
const labels=['Deposit balance (INR)','Loan outstanding (INR)','Loan-to-deposit ratio','90+ DPD exposure ratio (proxy)','Net interest income (INR)','Fee income (INR)','Operating expenses (INR)','Operating profit before losses/tax (INR)','Cost-to-income ratio','Annual transactions','Digital transaction share'];
const formulas=["='Monthly'!C13","='Monthly'!D13",'=B7/B6',"='Monthly'!E13/B7","=SUM('Monthly'!J2:J13)","=SUM('Monthly'!H2:H13)","=SUM('Monthly'!I2:I13)",'=B10+B11-B12','=B12/(B10+B11)',"=SUM('Channels'!B2:B5)","=SUMIFS('Channels'!B2:B5,'Channels'!A2:A5,\"Mobile\")/B15+SUMIFS('Channels'!B2:B5,'Channels'!A2:A5,\"Internet\")/B15"];
labels.forEach((label,i)=>{let r=i+6;summary.getRange(`A${r}`).values=[[label]];summary.getRange(`B${r}`).formulas=[[formulas[i]]];summary.getRange(`C${r}`).values=[[i<4?'31 December 2025':'January-December 2025']];});
summary.getRange('B6:B16').setNumberFormat('#,##0.00');for(const r of [8,9,14,16])summary.getRange(`B${r}`).setNumberFormat('0.0%');summary.getRange('B15').setNumberFormat('#,##0');summary.getRange('A13:C13').format.fill='#e8f0f7';summary.getRange('A13:B13').format.font.bold=true;
summary.getRange('A19').values=[['Operating profit excludes credit losses and tax.']];summary.getRange('A20').values=[['90+ DPD is an analytical proxy, not regulatory NPA.']];summary.getRange('A19:A20').format.font.color='#64748b';
const line=m.charts.add('line',[m.getRange('A1:A13'),m.getRange('C1:C13'),m.getRange('D1:D13')]);line.title='Month-end deposits and loans';line.setPosition('M2','V17');line.yAxis={numberFormatCode:'0,," M"',numberFormatSourceLinked:false};
const profit=m.charts.add('bar',[m.getRange('A1:A13'),m.getRange('K1:K13')]);profit.title='Monthly operating profit before losses/tax';profit.setPosition('M19','V34');profit.yAxis={numberFormatCode:'0,," M"',numberFormatSourceLinked:false};
const ch=summary.charts.add('line',[m.getRange('A1:A13'),m.getRange('C1:C13'),m.getRange('D1:D13')]);ch.title='Month-end balances (INR million)';ch.setPosition('E5','L20');ch.yAxis={numberFormatCode:'0,,',numberFormatSourceLinked:false};
const br=b.charts.add('bar',[b.getRange('B1:B9'),b.getRange('E1:E9')]);br.title='Branch deposit balances (INR million)';br.setPosition('P2','Y18');br.yAxis={numberFormatCode:'0,,',numberFormatSourceLinked:false};
const risk=wb.worksheets.getItem('Risk');const rc=risk.charts.add('bar',[risk.getRange('A1:A4'),risk.getRange('E1:E4')]);rc.title='90+ DPD loan rate';rc.setPosition('H2','O17');rc.yAxis={numberFormatCode:'0%',numberFormatSourceLinked:false};
const channels=wb.worksheets.getItem('Channels');const cc=channels.charts.add('bar',channels.getRange('A1:B5'));cc.title='Transaction count by channel';cc.setPosition('F2','M17');
wb.recalculate();
const expected=[k.deposit_balance,k.loan_outstanding,k.loan_to_deposit_ratio,k.dpd90_exposure_ratio,k.net_interest_income,k.fee_income,k.operating_expense,k.operating_profit,k.cost_to_income_ratio,k.transaction_count,k.digital_share];
const actual=summary.getRange('B6:B16').values.flat();actual.forEach((v,i)=>{if(typeof v!=='number'||Math.abs(v-expected[i])>Math.max(.02,Math.abs(expected[i])*1e-9))throw new Error(`KPI mismatch ${labels[i]}: ${v} vs ${expected[i]}`)});
// Verify an input change reaches the summary, then restore.
const old=m.getRange('F2').values[0][0];m.getRange('F2').values=[[old+1000]];wb.recalculate();if(Math.abs(summary.getRange('B13').values[0][0]-k.operating_profit-1000)>.02)throw new Error('Input propagation failed');m.getRange('F2').values=[[old]];wb.recalculate();
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!',options:{useRegex:true,maxResults:20},summary:'Formula error scan'})).ndjson);
for(const [name,range] of [['Overview','A1:L21'],['Monthly','A1:K14'],['Branches','A1:N10'],['Risk','A1:O18'],['Channels','A1:M18']]){
 const preview=await wb.render({sheetName:name,range,scale:1.3,format:'png'});await fs.writeFile(`${root}/outputs/charts/workbook_${name}.png`,new Uint8Array(await preview.arrayBuffer()));
}
const x=await SpreadsheetFile.exportXlsx(wb);await x.save(root+'/outputs/Banking_Analytics.xlsx');console.log('Excel exported; 11 KPIs reconcile and input propagation passes');
