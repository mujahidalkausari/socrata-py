from socrata import Socrata
from socrata.authorization import Authorization
from test.auth import auth, TestCase

class TestSource(TestCase):
    # def test_create_source(self):
    #     rev = self.create_rev()

    #     (ok, source) = rev.create_upload('foo.csv')
    #     self.assertTrue(ok)
    #     self.assertEqual(source.attributes['source_type']['filename'], 'foo.csv')

    #     assert 'show' in source.list_operations()
    #     assert 'bytes' in source.list_operations()

    # def test_upload_csv(self):
    #     rev = self.create_rev()
    #     (ok, source) = rev.create_upload('foo.csv')
    #     assert ok

    #     with open('test/fixtures/simple.csv', 'rb') as f:
    #         (ok, input_schema) = source.csv(f)
    #         self.assertTrue(ok)
    #         self.assertEqual(input_schema.attributes['total_rows'], 4)

    #         names = sorted([ic['field_name'] for ic in input_schema.attributes['input_columns']])
    #         self.assertEqual(['a', 'b', 'c'], names)

    #         assert 'show' in input_schema.list_operations()

    # def test_create_source_outside_rev(self):
    #     pub = Socrata(auth)

    #     (ok, source) = pub.sources.create_upload('foo.csv')
    #     self.assertTrue(ok, source)
    #     self.assertEqual(source.attributes['source_type']['filename'], 'foo.csv')

    #     assert 'show' in source.list_operations()
    #     assert 'bytes' in source.list_operations()

    # def test_upload_csv_outside_rev(self):
    #     pub = Socrata(auth)

    #     (ok, source) = pub.sources.create_upload('foo.csv')
    #     self.assertTrue(ok, source)

    #     with open('test/fixtures/simple.csv', 'rb') as f:
    #         (ok, input_schema) = source.csv(f)
    #         self.assertTrue(ok, input_schema)
    #         names = sorted([ic['field_name'] for ic in input_schema.attributes['input_columns']])
    #         self.assertEqual(['a', 'b', 'c'], names)

    # def test_put_source_in_revision(self):
    #     pub = Socrata(auth)

    #     (ok, source) = pub.sources.create_upload('foo.csv')
    #     self.assertTrue(ok, source)

    #     with open('test/fixtures/simple.csv', 'rb') as f:
    #         (ok, input_schema) = source.csv(f)
    #         self.assertTrue(ok, input_schema)

    #         rev = self.create_rev()

    #         (ok, source) = source.add_to_revision(rev)
    #         self.assertTrue(ok, source)


    def test_source_change_header_rows(self):
        pub = Socrata(auth)
        (ok, source) = pub.sources.create_upload('foo.csv')
        self.assertTrue(ok, source)

        (ok, source) = source\
            .change_parse_option('header_count').to(2)\
            .change_parse_option('column_header').to(2)\
            .run()

        self.assertTrue(ok, source)

        po = source.attributes['parse_options']
        self.assertEqual(po['header_count'], 2)
        self.assertEqual(po['column_header'], 2)

    def test_source_change_on_existing_upload(self):
        pub = Socrata(auth)
        (ok, source) = pub.sources.create_upload('foo.csv')
        self.assertTrue(ok, source)

        with open('test/fixtures/skip-header.csv', 'rb') as f:
            (ok, input_schema) = source.csv(f)
            self.assertTrue(ok, input_schema)


        (ok, source) = source\
            .change_parse_option('header_count').to(2)\
            .change_parse_option('column_header').to(2)\
            .run()

        self.assertTrue(ok, source)

        po = source.attributes['parse_options']
        self.assertEqual(po['header_count'], 2)
        self.assertEqual(po['column_header'], 2)

        (ok, input_schema) = source.latest_input()
        self.assertTrue(ok, input_schema)
        (ok, output_schema) = input_schema.latest_output()
        self.assertTrue(ok, output_schema)

        [a, b, c] = output_schema.attributes['output_columns']

        self.assertEqual(a['field_name'], 'a')
        self.assertEqual(b['field_name'], 'b')
        self.assertEqual(c['field_name'], 'c')
