#!/usr/bin/env python3
import scroller
import sys
from unittest import TestCase, main
from unittest.mock import patch, call


class ScrollerTest(TestCase):
    _TEST_STRING = 'argument clinic'
    _TEST_STRING_PERMUTED = 'rgument clinica'

    def setUp(self):
        self.test_str = self.__class__._TEST_STRING
        self.test_str_permuted = self.__class__._TEST_STRING_PERMUTED

    def test_permute(self):
        string = scroller.permute(self.test_str)
        self.assertEqual(string, self.test_str_permuted)
        string = scroller.permute(string, rev=True)
        self.assertEqual(string, self.test_str)

    def test_scroll(self):
        scrolled = scroller.scroll(self.test_str)
        string = self.test_str
        for _ in range(len(self.test_str)):
            string = scroller.permute(string)
            self.assertEqual(next(scrolled), string)

    def test_scroll_reverse(self):
        scrolled = scroller.scroll(self.test_str)
        test_length = len(self.test_str) - 1
        for _ in range(test_length):
            string = next(scrolled)
        scrolled = scroller.scroll(string, rev=True)
        for _ in range(test_length):
            string = next(scrolled)
        self.assertEqual(string, self.test_str)

    def test_scroll_separator(self):
        sep = ' '
        scrolled = scroller.scroll(self.test_str, sep=sep)
        string = self.test_str + sep
        for _ in range(len(self.test_str)):
            string = scroller.permute(string)
            self.assertEqual(next(scrolled), string)

    def test_scroll_separator_when_reversed(self):
        sep = ' '
        scrolled = scroller.scroll(self.test_str, sep=sep, rev=True)
        string = self.test_str + sep
        for i in range(len(self.test_str)):
            string = scroller.permute(string, rev=True)
            self.assertEqual(next(scrolled), string)

    def test_scroll_static(self):
        scrolled = scroller.scroll(self.test_str, static=True)
        for i in range(len(self.test_str)):
            self.assertEqual(next(scrolled), self.test_str)

    def test_scroll_static_when_reversed(self):
        scrolled = scroller.scroll(self.test_str, static=True, rev=True)
        for i in range(len(self.test_str)):
            self.assertEqual(next(scrolled), self.test_str)

    def test_scroller_count(self):
        s = scroller.scroller(self.test_str, count=len(self.test_str))
        string = self.test_str
        for x in s:
            string = x
        self.assertEqual(string, self.test_str)

    def test_scroller(self):
        s = scroller.scroller(self.test_str, count=len(self.test_str))
        e = self.test_str
        for a in s:
            e = scroller.permute(e)
            self.assertEqual(a, e)

    def test_scroller_when_reversed(self):
        s = scroller.scroller(
                self.test_str,
                count=len(self.test_str),
                rev=True
        )
        e = self.test_str
        for a in s:
            e = scroller.permute(e, rev=True)
            self.assertEqual(a, e)

    def test_scroller_static(self):
        s = scroller.scroller(
                self.test_str,
                count=len(self.test_str),
                static=True
        )
        e = self.test_str
        for a in s:
            self.assertEqual(a, e)

    def test_scroller_static_when_reversed(self):
        s = scroller.scroller(self.test_str, count=3, static=True, rev=True)
        e = self.test_str
        for a in s:
            self.assertEqual(a, e)


class ScrollerCLITest(TestCase):
    _TEST_STRING = 'gumby brain specialist'

    def setUp(self):
        self.test_str = self.__class__._TEST_STRING

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_count(self, mock_print, mock_sleep):
        c = 5
        args = scroller.parser.parse_args(['-c', str(c)])
        scroller.main(self.test_str, args)
        self.assertEqual(mock_print.call_count, c)

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_length_when_should_not_be_static(self, mock_print, mock_sleep):
        l = len(self.test_str)
        args = scroller.parser.parse_args(['-l', str(l), '-c', '5'])
        scroller.main(self.test_str, args)
        self.assertNotEqual(mock_print.call_args, self.test_str)

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_length_when_should_be_static(self, mock_print, mock_sleep):
        l = len(self.test_str) + 2
        c = 2
        args = scroller.parser.parse_args([
            '-l', str(l),
            '-c', str(c),
            '-s', ''
        ])
        scroller.main(self.test_str, args)
        expected_call = call(self.test_str, end='\r')
        mock_print.assert_has_calls([expected_call for i in range(c)])

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_interval(self, mock_print, mock_sleep):
        i = 2
        args = scroller.parser.parse_args(['-c', '1', '-i', str(i)])
        scroller.main(self.test_str, args)
        mock_sleep.assert_called_with(i)

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_reverse(self, mock_print, mock_sleep):
        args = scroller.parser.parse_args(['-c', '1', '-s', '', '-r'])
        scroller.main(self.test_str, args)
        (calling_args,), _ = mock_print.call_args
        p = scroller.permute(self.test_str, rev=True)
        self.assertEqual(calling_args, p)

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_separator(self, mock_print, mock_sleep):
        s = '_'
        args = scroller.parser.parse_args(['-c', '1', '-s', s, '-r'])
        scroller.main(self.test_str, args)
        (calling_args,), _ = mock_print.call_args
        self.assertEqual(calling_args, s + self.test_str)

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_newline(self, mock_print, mock_sleep):
        args = scroller.parser.parse_args(['-c', '1', '-n'])
        scroller.main(' ', args)
        _, calling_kwargs = mock_print.call_args
        self.assertEqual(calling_kwargs['end'], '\n')

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    @patch('sys.stdout.write', autospe=True)
    @patch('builtins.input', autospec=True)
    @patch('select.select', autospec=True)
    def test_open(self, mock_select, mock_input, mock_write,
                  mock_print, mock_sleep):
        mock_input.side_effect = ['life of brian', 'flying circus']

        def gen_side_effect():
            yield ([sys.stdin], [], [])
            while True:
                yield ([], [], [])

        mock_select.side_effect = gen_side_effect()
        args = scroller.parser.parse_args(['-c', '2', '-n', '-o'])
        scroller.main(args=args)
        self.assertEqual(mock_input.call_count, 2)
        self.assertTrue(mock_write.called)
        self.assertTrue(mock_sleep.called)

if __name__ == '__main__':
    main()
