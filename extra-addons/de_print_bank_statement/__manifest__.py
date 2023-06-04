
{
  "name"                 :  "Print Bank Statement",
  "summary"              :  "This App will Add Print Option in Cash/Bank Statement",
  "category"             :  "Accounting",
  "version"              :  "1.1",
  "sequence"             :  1,
  "author"               :  "Pandora Desgin",
  "license"              :  "OPL-1",
  "website"              :  "https://pandoratech.ae",
  "description"          :  """
This App will Add Print Option in Cash/Bank Statement
""",
  "live_test_url"        :  "",
  "depends"              :  [
                             'account'
                            ],
  "data"                 :  [
                             'views/statement_report.xml',
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  0,
  "currency"             :  "EUR",
  "images"		 :['static/description/banner.jpg'],
}