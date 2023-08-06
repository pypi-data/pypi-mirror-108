import os
import re
import urllib.parse
from typing import Tuple, List

from dict2anki import htmls
from dict2anki.net import url_get_content, urlopen_with_retry, fake_headers, url_save, url_save_guess_file
from dict2anki.utils import Log, valid_path, get_tag
from .extractor import CardExtractor, WordNotFoundError, ExtractError

__all__ = [
    'CambridgeExtractor',
]

TAG = get_tag(__name__)

DEFAULT_OUT_PATH = os.path.join(os.curdir, TAG)

DEFAULT_FRONT_TEMPLATE = '''<hr>
<div style="text-align:center">{{正面}}</div>'''

# 'https://dictionary.cambridge.org/zhs/%E6%90%9C%E7%B4%A2/direct/?datasetsearch=english-chinese-simplified&q={}'

URL_ROOT = 'https://dictionary.cambridge.org/'

URL_QUERY = 'https://dictionary.cambridge.org/zhs/' \
            '%E8%AF%8D%E5%85%B8/%E8%8B%B1%E8%AF%AD-%E6%B1%89%E8%AF%AD-%E7%AE%80%E4%BD%93/{}'

URL_STYLE = 'https://dictionary.cambridge.org/zhs/common.css'

URL_FONT = 'https://dictionary.cambridge.org/zhs/external/fonts/cdoicons.woff'

URL_AMP = 'https://cdn.ampproject.org/v0.js'

URL_AMP_AUDIO = 'https://cdn.ampproject.org/v0/amp-audio-0.1.js'

URL_AMP_ACCORDION = 'https://cdn.ampproject.org/v0/amp-accordion-0.1.js'

THRESHOLD_COLLAPSE = 4096

HTML_COLLAPSE = '<amp-accordion><section>{}</section></amp-accordion>'

HTML_COLLAPSE1 = '<amp-accordion><section>' \
                 '<header class="ca_h daccord_h"><i class="i i-plus ca_hi"></i>{}</header>{}' \
                 '</section></amp-accordion>'

parse_tag = re.compile(r'^(<[\s\S]*?>)([\s\S]*)(</[\s\S]*>)$')


class CambridgeExtractor(CardExtractor):

    def __init__(self, out_path: str = DEFAULT_OUT_PATH, **kwargs):
        super().__init__(out_path, **kwargs)
        self._front_template = DEFAULT_FRONT_TEMPLATE
        self._styling = None

    def generate_styling(self):
        if not self._styling:
            self._styling = self._retrieve_styling()
        super().generate_styling()

    def _retrieve_styling(self) -> str:
        Log.i(TAG, 'retrieving styling')
        style = url_get_content(URL_STYLE, fake_headers())
        font = url_save_guess_file(URL_FONT, fake_headers())[0]
        # add '_' to tell Anki that the file is used by template
        _font = url_save(
            URL_FONT,
            headers=fake_headers(),
            filename=valid_path(os.path.join(self.media_path, '_' + font)),
            force=True
        )[0]
        Log.i(TAG, 'saved font file to: {}'.format(_font))
        _font = os.path.basename(_font)
        style = re.sub(r'url\([\S]*?/{}'.format(font), 'url({}'.format(_font), style)
        style = '<style>{}</style>\n'.format(style)
        style += '<script type="text/javascript">{}</script>\n'.format(
            url_get_content(URL_AMP, fake_headers()).replace('\n', ' ')
        )
        style += '<script type="text/javascript">{}</script>\n'.format(
            url_get_content(URL_AMP_AUDIO, fake_headers()).replace('\n', ' ')
        )
        style += '<script type="text/javascript">{}</script>\n'.format(
            url_get_content(URL_AMP_ACCORDION, fake_headers()).replace('\n', ' ')
        )
        Log.i(TAG, 'retrieved styling')
        return style

    def get_card(self, word: str) -> Tuple[str, List[str]]:
        Log.d(TAG, 'querying "{}"'.format(word))
        response = urlopen_with_retry(
            URL_QUERY.format(urllib.parse.quote(word.replace('/', ' '))),
            fake_headers()
        )
        actual = urllib.parse.urlsplit(response.geturl()).path.rsplit('/', 1)[-1]
        actual = ' '.join(actual.split('-'))
        if not actual:
            raise WordNotFoundError('can\'t find: "{}"'.format(word))
        if actual != ' '.join(word.replace('/', ' ').replace('-', ' ').replace('\'', ' ').lower().split()):
            Log.i(TAG, 'redirected to: "{}"'.format(actual))
        content = url_get_content(response, fake_headers())
        fields = self._extract_fields(content)
        Log.d(TAG, 'parsed: "{}"'.format(actual))
        return actual, fields

    def _extract_fields(self, html_str: str) -> List[str]:
        try:
            back = htmls.find(html_str, 'div', 'class="di-body"')
            front = htmls.find(back, 'div', 'class="di-title"')

            # remove titles
            back = htmls.removeall(back, 'div', 'class="di-title"')
            # # remove audios
            # back = htmls.removeall(back, 'span', 'class="daud"')
            # support online audios
            back = re.sub(r'src="/zhs/media', 'src="{}zhs/media'.format(URL_ROOT), back)
            # remove phrases and idioms
            back = htmls.removeall(back, 'div', 'class="xref')
            # seems useless
            back = htmls.removeall(back, 'div', 'class="cid"')
            back = htmls.removeall(back, 'div', 'class="dwl hax"')

            def remove_tag(h):
                return parse_tag.sub(r'\g<2>', h)

            # remove links
            back = htmls.sub(back, remove_tag, 'a', 'class="query"')
            back = htmls.sub(back, remove_tag, 'a', 'href=')

            # remove share
            back = htmls.removeall(back, 'div', 'class="hfr lpb-2"')
            # remove more examples
            back = htmls.removeall(back, 'div', 'class="daccord"')
            # remove js
            back = htmls.removeall(back, 'script')
            # remove underlines
            back = htmls.sub(back, remove_tag, 'span', 'class="x-h dx-h"')
            # remove adds
            back = htmls.removeall(back, 'div', 'ad_contentslot')
            back = htmls.removeall(back, 'div', 'class="bb hax"')
            # collapse long cards
            if len(back) > THRESHOLD_COLLAPSE:
                back = self._collapse(back)
            return [front, back]
        except Exception as e:
            raise ExtractError('can\'t extract fields', e)

    def _collapse(self, html_str: str) -> str:
        def collapse1(h):
            header = htmls.find(htmls.find(h, 'div', 'def-body ddef_b'), 'span', 'trans dtrans dtrans-se')
            return HTML_COLLAPSE1.format(header, h)

        html_str = htmls.sub(html_str, collapse1, 'div', 'def-block ddef_block')

        def collapse2(h):
            m = parse_tag.match(h)
            Log.d(TAG, '{}\n{}\n{}'.format(m.group(1), m.group(2), m.group(3)))
            return m.group(1) + HTML_COLLAPSE.format(m.group(2)) + m.group(3)

        # these were removed
        # html_str = htmls.sub(html_str, collapse2, 'div', 'xref phrasal_verbs hax dxref-w lmt-25 lmb-25')
        # html_str = htmls.sub(html_str, collapse2, 'div', 'xref idioms hax dxref-w lmt-25 lmb-25')
        return html_str
