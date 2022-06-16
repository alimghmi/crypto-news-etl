import logger
import scraper
import serializer


log = logger.get('app')


def app():
    engine = scraper.Scraper()
    extracted = engine.run()
    if not extracted:
        log.error('data extraction failed')
        return False

    log.info('data extracted successfully')
    transofrm = serializer.Serializer(extracted)
    if not transofrm.validate():
        log.error('data validation failed')
        return False

    log.info('data validated successfully')
    output = transofrm.load()
    log.info('data loaded successfully')


if __name__ == '__main__':
    app()