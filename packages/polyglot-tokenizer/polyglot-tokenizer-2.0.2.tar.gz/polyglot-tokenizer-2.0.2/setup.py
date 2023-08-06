# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['polyglot_tokenizer', 'polyglot_tokenizer.tests']

package_data = \
{'': ['*'], 'polyglot_tokenizer': ['data/*']}

install_requires = \
['pbr>=2.0,<3.0', 'six>=1.12,<2.0']

entry_points = \
{'console_scripts': ['polyglot-tokenizer = polyglot_tokenizer:main']}

setup_kwargs = {
    'name': 'polyglot-tokenizer',
    'version': '2.0.2',
    'description': "Tokenizer for world's most spoken languages and social media texts like Facebook, Twitter etc.",
    'long_description': 'Polyglot Tokenizer\n==================\n\n\nTokenizer for world\'s most spoken languages and social media texts like Facebook, Twitter etc.\n\n\nInstallation\n------------\n\n::\n\n    pip install polyglot-tokenizer\n\nExamples\n--------\n\nWithin Python\n^^^^^^^^^^^^^\n\n\n.. code:: python\n\n    >>> from __future__ import unicode_literals\n    >>> from polyglot_tokenizer import Tokenizer\n    >>> tk = Tokenizer(lang=\'en\', smt=True) #smt is a flag for social-media-text\n    >>> text = "RT @BJP_RSS Crack down on Black money.India slides to 75th slot on Swiss bank money list #ModiForeignAchievements @RituRathaur https://t.c…"\n    >>> tk.tokenize(text)\n    [\'RT\', \'@BJP_RSS\', \'Crack\', \'down\', \'on\', \'Black\', \'money\', \'.\', \'India\', \'slides\', \'to\', \'75th\', \'slot\', \'on\', \'Swiss\', \'bank\', \'money\', \'list\', \'#ModiForeignAchievements\', \'@RituRathaur\', \'https://t.c…\']\n    >>> tk = Tokenizer(lang=\'hi\')\n    >>> tk.tokenize("22 साल के लंबे इंतजार के बाद आखिरकार हॉलीवुड स्टार लियोनार्डो डिकैप्रियो को अपनी पहली ऑस्कर ट्रॉफी"\n    ...             " मिल चुकी है। उन्हें ये अवॉर्ड अपनी फिल्म ‘द रेवेनेंट’ में ह्यूज ग्लास के किरदार के लिए मिला, लेकिन उनके"\n    ...             " के लिए रोल निभाना आसान नहीं था।")\n    [\'22\', \'साल\', \'के\', \'लंबे\', \'इंतजार\', \'के\', \'बाद\', \'आखिरकार\', \'हॉलीवुड\', \'स्टार\', \'लियोनार्डो\', \'डिकैप्रियो\', \'को\', \'अपनी\', \'पहली\', \'ऑस्कर\', \'ट्रॉफी\', \'मिल\', \'चुकी\', \'है\', \'।\', \'उन्हें\', \'ये\', \'अवॉर्ड\', \'अपनी\', \'फिल्म\', "\'", \'द\', \'रेवेनेंट\', "\'", \'में\', \'ह्यूज\', \'ग्लास\', \'के\', \'किरदार\', \'के\', \'लिए\', \'मिला\', \',\', \'लेकिन\', \'उनके\', \'के\', \'लिए\', \'रोल\', \'निभाना\', \'आसान\', \'नहीं\', \'था\', \'।\']\n    >>> tk = Tokenizer(lang=\'hi\', split_sen=True)\n    >>> tk.tokenize("22 साल के लंबे इंतजार के बाद आखिरकार हॉलीवुड स्टार लियोनार्डो डिकैप्रियो को अपनी पहली ऑस्कर ट्रॉफी"\n    ...             " मिल चुकी है। उन्हें ये अवॉर्ड अपनी फिल्म ‘द रेवेनेंट’ में ह्यूज ग्लास के किरदार के लिए मिला, लेकिन उनके"\n    ...             " के लिए रोल निभाना आसान नहीं था। फिल्म एक सीन के लिए लियोनार्डो को भैंस का कच्चा लीवर खाना"\n    ...             " पड़ा था। जबकि असल जिंदगी में वो पूरी तरह शाकाहारी हैं। हालांकि इस सीन के लिए पहले लियोनार्डो को"\n    ...             " मांस जैसे दिखने वाली चीज दी गई थी, लेकिन उन्हें लगा कि ऐसा करना गलत होगा। फिल्म के लिए इम्पोर्ट"\n    ...             " की गई चीटियां...")\n    [[\'22\', \'साल\', \'के\', \'लंबे\', \'इंतजार\', \'के\', \'बाद\', \'आखिरकार\', \'हॉलीवुड\', \'स्टार\', \'लियोनार्डो\', \'डिकैप्रियो\', \'को\', \'अपनी\', \'पहली\', \'ऑस्कर\', \'ट्रॉफी\', \'मिल\', \'चुकी\', \'है\', \'।\'], [\'उन्हें\', \'ये\', \'अवॉर्ड\', \'अपनी\', \'फिल्म\', "\'", \'द\', \'रेवेनेंट\', "\'", \'में\', \'ह्यूज\', \'ग्लास\', \'के\', \'किरदार\', \'के\', \'लिए\', \'मिला\', \',\', \'लेकिन\', \'उनके\', \'के\', \'लिए\', \'रोल\', \'निभाना\', \'आसान\', \'नहीं\', \'था\', \'।\'], [\'फिल्म\', \'एक\', \'सीन\', \'के\', \'लिए\', \'लियोनार्डो\', \'को\', \'भैंस\', \'का\', \'कच्चा\', \'लीवर\', \'खाना\', \'पड़ा\', \'था\', \'।\'], [\'जबकि\', \'असल\', \'जिंदगी\', \'में\', \'वो\', \'पूरी\', \'तरह\', \'शाकाहारी\', \'हैं\', \'।\'], [\'हालांकि\', \'इस\', \'सीन\', \'के\', \'लिए\', \'पहले\', \'लियोनार्डो\', \'को\', \'मांस\', \'जैसे\', \'दिखने\', \'वाली\', \'चीज\', \'दी\', \'गई\', \'थी\', \',\', \'लेकिन\', \'उन्हें\', \'लगा\', \'कि\', \'ऐसा\', \'करना\', \'गलत\', \'होगा\', \'।\'], [\'फिल्म\', \'के\', \'लिए\', \'इम्पोर्ट\', \'की\', \'गई\', \'चीटियां\', \'...\']]\n\n\nFrom Console\n^^^^^^^^^^^^\n\n.. parsed-literal::\n\n    polyglot-tokenizer --h\n\n    usage: polyglot-tokenizer [-h] [-v] [-i] [-s] [-t] [-o] [-l]\n    \n    Tokenizer for world\'s most spoken languages\n\n    \n    optional arguments:\n      -h, --help            show this help message and exit\n      -v, --version         show program\'s version number and exit\n      -i , --input          <input-file>\n      -s, --split-sentences\n                            set this flag to apply sentence segmentation\n      -t, --social-media-test\n                            set this flag if the input file contains social media\n                            text like twitter, facebook and whatsapp\n      -o , --output         <output-file>\n      -l , --language       select language (2 letter ISO-639 code) {hi, ur, bn,\n                            as, gu, ml, pa, te, ta, kn, or, mr, cu, myv, nn, yi,\n                            ne, bo, br, ks, en, es, ca, cs, de, el, en, fi, da,\n                            eu, kok, nb, uz, fr, ga, hu, is, it, lt, lv, nl, pl,\n                            pt, ro, ru, sk, bm, yue, mk, ku, sl, sv, zh, et, fo,\n                            gl, hsb, af, ar, be, hy, bg, ka, ug, hr, mn, tk, kk,\n                            ky, la, no, fa, uk, tl, tr, vi, yo, ko, got, ckb, he,\n                            id, sr}\n\n    Example ::\n\n    polyglot-tokenizer < raw_file.txt -l en -s > tokenized.txt\n\n\n\n\n',
    'author': 'irshadbhat',
    'author_email': 'bhatirshad127@gmail.com',
    'url': 'https://github.com/irshadbhat/polyglot-tokenizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
