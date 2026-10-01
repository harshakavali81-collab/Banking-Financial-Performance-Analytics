// Blank Query named LoadCsv. Define a Text parameter DataFolder first.
(FileName as text) as table =>
let
    Source = Csv.Document(File.Contents(DataFolder & "/" & FileName), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    Headers
