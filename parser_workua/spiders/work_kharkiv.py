import scrapy


class WorkKharkivSpider(scrapy.Spider):
    name = 'work_kharkiv'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    def parse(self, response):
        for item in response.css('div#pjax-resume-list div.card.resume-link'):

            worker_card_uri = item.css('h2 a::attr(href)').get()

            result_pars = dict(

                name=item.css('div b::text').get().strip(),
                age=None,
                position=item.css('h2 a::text').get()
            )
            yield response.follow(worker_card_uri, self.parse_person, meta={
                'result': result_pars
            })

        for page in response.css('ul.pagination li'):
            if page.css('a::text').get() == 'Наступна':
                yield response.follow(
                    page.css('a::attr(href)').get(),
                    self.parse
                )

    def parse_person(self, response):

        age = response.css('div.card dd::text').get()[:2]
        header = response.css('div.card > h2::text').get()
        description = ' '.join(response.css('div.card > p::text').getall())
        description = header + " " + ' '.join(description.split())

        people_information = response.meta['result']
        people_information['age'] = age
        people_information['description'] = description

        yield people_information