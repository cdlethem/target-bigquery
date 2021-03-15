from tests import unittestcore


class TestSimpleStreamLoadJob(unittestcore.BaseUnitTest):

    def test_simple_stream(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/simple_stream.json",
            config="../sandbox/target_config.json",
            processhandler="load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
        self.assertDictEqual(state, {"bookmarks": {"simple_stream": {"timestamp": "2020-01-11T00:00:00.000000Z"}}})

        table = self.client.get_table("{}.simple_stream".format(self.dataset_id))
        self.assertEqual(3, table.num_rows, msg="Number of rows mismatch")
        self.assertIsNone(table.clustering_fields)
        self.assertIsNone(table.partitioning_type)

    def test_simple_stream_with_tables_config(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/simple_stream.json",
            config="../sandbox/target_config.json",
            tables="./rsc/simple_stream_table_config.json",
            processhandler="load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
        self.assertDictEqual(state, {"bookmarks": {"simple_stream": {"timestamp": "2020-01-11T00:00:00.000000Z"}}})

        table = self.client.get_table("{}.simple_stream".format(self.dataset_id))
        self.assertEqual(3, table.num_rows, msg="Number of rows mismatch")
        self.assertIsNotNone(table.clustering_fields)
        self.assertIsNotNone(table.partitioning_type)


class TestSimpleStreamPartialLoadJob(unittestcore.BaseUnitTest):

    def test_simple_stream(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/simple_stream.json",
            config="../sandbox/target_config.json",
            processhandler="partial-load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
        self.assertDictEqual(state, {"bookmarks": {"simple_stream": {"timestamp": "2020-01-11T00:00:00.000000Z"}}})

        table = self.client.get_table("{}.simple_stream".format(self.dataset_id))
        self.assertEqual(3, table.num_rows, msg="Number of rows mismatch")
        self.assertIsNone(table.clustering_fields)
        self.assertIsNone(table.partitioning_type)

    def test_simple_stream_with_tables_config(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/simple_stream.json",
            config="../sandbox/target_config.json",
            tables="./rsc/simple_stream_table_config.json",
            processhandler="partial-load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
        self.assertDictEqual(state, {"bookmarks": {"simple_stream": {"timestamp": "2020-01-11T00:00:00.000000Z"}}})

        table = self.client.get_table("{}.simple_stream".format(self.dataset_id))
        self.assertEqual(3, table.num_rows, msg="Number of rows mismatch")
        self.assertIsNotNone(table.clustering_fields)
        self.assertIsNotNone(table.partitioning_type)


class TestSimpleStreamBookmarksPartialLoadJob(unittestcore.BaseUnitTest):

    def test_simple_stream(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/simple_stream.json",
            config="../sandbox/target_config.json",
            processhandler="bookmarks-partial-load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
        self.assertDictEqual(state, {"bookmarks": {"simple_stream": {"timestamp": "2020-01-11T00:00:00.000000Z"}}})

        table = self.client.get_table("{}.simple_stream".format(self.dataset_id))
        self.assertEqual(3, table.num_rows, msg="Number of rows mismatch")
        self.assertIsNone(table.clustering_fields)
        self.assertIsNone(table.partitioning_type)

    def test_simple_stream_with_tables_config(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/simple_stream.json",
            config="../sandbox/target_config.json",
            tables="./rsc/simple_stream_table_config.json",
            processhandler="bookmarks-partial-load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
        self.assertDictEqual(state, {"bookmarks": {"simple_stream": {"timestamp": "2020-01-11T00:00:00.000000Z"}}})

        table = self.client.get_table("{}.simple_stream".format(self.dataset_id))
        self.assertEqual(3, table.num_rows, msg="Number of rows mismatch")
        self.assertIsNotNone(table.clustering_fields)
        self.assertIsNotNone(table.partitioning_type)

