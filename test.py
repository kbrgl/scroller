#!/usr/bin/env python3
import scroller
from unittest import TestCase, main
from unittest.mock import patch, call

class ScrollerTest(TestCase):
    _TEST_STRING = 'argument clinic' # https://www.youtube.com/watch?v=kQFKtI6gn9Y
    _TEST_STRING_PERMUTED = 'rgument clinica'
    _TEST_STRING_REV_PERMUTED = 'cargument clini'

    def test_permute(self):
        self.assertEqual(scroller.permute(ScrollerTest._TEST_STRING), ScrollerTest._TEST_STRING_PERMUTED)
        self.assertEqual(scroller.permute(ScrollerTest._TEST_STRING, rev=True), ScrollerTest._TEST_STRING_REV_PERMUTED)

    def test_scroll(self):
        scrolled = scroller.scroll(ScrollerTest._TEST_STRING)
        string = ScrollerTest._TEST_STRING
        for _ in range(3):
            string = scroller.permute(string)
            self.assertEqual(next(scrolled), string)

    def test_scroll_rev(self):
        scrolled = scroller.scroll(ScrollerTest._TEST_STRING, rev=True)
        string = ScrollerTest._TEST_STRING
        for _ in range(3):
            string = scroller.permute(string, rev=True)
            self.assertEqual(next(scrolled), string)

    def test_scroll_sep(self):
        sep = ' '
        scrolled = scroller.scroll(ScrollerTest._TEST_STRING, sep=sep)
        string = ScrollerTest._TEST_STRING + sep
        for _ in range(3):
            string = scroller.permute(string)
            self.assertEqual(next(scrolled), string)

    def test_scroll_sep_rev(self):
        sep = ' '
        scrolled = scroller.scroll(ScrollerTest._TEST_STRING, sep=sep, rev=True)
        string = ScrollerTest._TEST_STRING + sep
        for i in range(3):
            string = scroller.permute(string, rev=True)
            self.assertEqual(next(scrolled), string)

    def test_scroll_static(self):
        scrolled = scroller.scroll(ScrollerTest._TEST_STRING, static=True)
        for i in range(3):
            self.assertEqual(next(scrolled), ScrollerTest._TEST_STRING)


class ScrollerCLITest(TestCase):
    _TEST_STRING = 'gumby brain specialist' # https://www.youtube.com/watch?v=XyFfmGf3b2Y
    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_count(self, mock_print, mock_sleep):
        c = 5
        args = scroller.parser.parse_args(['-c', str(c)])
        scroller.main(ScrollerCLITest._TEST_STRING, args)
        self.assertEqual(mock_print.call_count, c)

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_length_when_should_not_be_static(self, mock_print, mock_sleep):
        l = len(ScrollerCLITest._TEST_STRING)
        args = scroller.parser.parse_args(['-l', str(l), '-c', '5'])
        scroller.main(ScrollerCLITest._TEST_STRING, args)
        self.assertNotEqual(mock_print.call_args, ScrollerCLITest._TEST_STRING)

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_length_when_should_be_static(self, mock_print, mock_sleep):
        l = len(ScrollerCLITest._TEST_STRING) + 2
        c = 2
        args = scroller.parser.parse_args(['-l', str(l), '-c', str(c), '-s', ''])
        scroller.main(ScrollerCLITest._TEST_STRING, args)
        expected_call = call(ScrollerCLITest._TEST_STRING, end='\r')
        mock_print.assert_has_calls([expected_call for i in range(c)])

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_interval(self, mock_print, mock_sleep):
        i = 2
        args = scroller.parser.parse_args(['-c', '1', '-i', str(i)])
        scroller.main(ScrollerCLITest._TEST_STRING, args)
        mock_sleep.assert_called_with(i)

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_reverse(self, mock_print, mock_sleep):
        args = scroller.parser.parse_args(['-c', '1', '-s', '', '-r'])
        scroller.main(ScrollerCLITest._TEST_STRING, args)
        (calling_args,), _ = mock_print.call_args
        self.assertEqual(calling_args, scroller.permute(ScrollerCLITest._TEST_STRING, rev=True))

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_separator(self, mock_print, mock_sleep):
        s = '_'
        args = scroller.parser.parse_args(['-c', '1', '-s', s, '-r'])
        scroller.main(ScrollerCLITest._TEST_STRING, args)
        (calling_args,), _ = mock_print.call_args
        self.assertEqual(calling_args, s + ScrollerCLITest._TEST_STRING)

    @patch('time.sleep', autospec=True)
    @patch('builtins.print', autospec=True)
    def test_newline(self, mock_print, mock_sleep):
        args = scroller.parser.parse_args(['-c', '1', '-n'])
        scroller.main(' ', args)
        _, calling_kwargs = mock_print.call_args
        self.assertEqual(calling_kwargs['end'], '\n')



if __name__ == '__main__':
    main()
