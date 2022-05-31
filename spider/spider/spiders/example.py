import scrapy
import gspread
import re
from tld import get_tld
class ExampleSpider(scrapy.Spider):
    name = 'example'
    greedy = True
    #allowed_domains = ['example.com']
    gc=gspread.service_account(filename=r"C:\Users\HP\Dropbox\PC\Desktop\LutronScraper\pcreds.json")

    sh=gc.open_by_url("https://docs.google.com/spreadsheets/d/10tSXDj3bmp4OXwbif3bN0_ffZkV_fsZPWycEs4wMOSw/edit#gid=1239982557")
    worksheet=sh.get_worksheet(1)
    values=worksheet.col_values(1)
    start_urls = ['https://www.systemvideo.com/','https://transactts.co.uk/LOCATIONS/']
    reg=''
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    forbidden_keys = ['tel:', 'mailto:', '.jpg', '.pdf', '.png']
    #[-.a-z]+@[^@\s\.]+\.[.a-z]{2,3}
    def parse(self, response):
        try:
            html = response.body.decode('utf-8')
        except UnicodeDecodeError:
            pass
            
        body_emails = self.email_regex.findall(html)
    
        emails = [email for email in body_emails if \
        get_tld('https://' + email.split('@')[-1], fail_silently=True)]
        
        
        yield {
            'emails': list(set(emails)),
            'page': response.request.url
        }
       