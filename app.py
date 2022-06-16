import scraper
import serializer


def app():
    engine = scraper.Scraper()
    extracted = engine.run()
    if not extracted:
        print('Err', 'No data from scraper')
        return False

    print('Success', 'Data Extracted')

    transofrm = serializer.Serializer(extracted)
    if not transofrm.validate():
        print('Err', 'Data validation failed')
        return False

    print('Success', 'Data validated')
    output = transofrm.load()

    print('Success', 'Data loaded to database')
    print(output)


if __name__ == '__main__':
    app()