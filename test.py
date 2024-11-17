import fitz
import re
import unicodedata


def is_english_word(word):
        """Check if the word contains only Latin characters."""
        for char in word:
            print (unicodedata.name(char, '') )


text = """
/ T '] — i L,/ ^ Atl/C-lt'.
2
.
/T Mearii san
*hU
hi; •?* Arizona daigaku no
ichinensee
Mearii san *6 & U I'
gakusee
gakusee
—* 'J
Mearii san
—
sannensee
^^ —^5 /C(i *X,fcX,-t£v'T-ttf'0 Mearii san wa sannensee desu ka.
^ n'A. lcteX,-tiA'T"fo lie, ninensee desu.
Q : A:
3. AltlS/C/IXJAL/C Takeshi san nihonjin
4. tz\mL/\zilLt-:^tH<n Takeshi san Nihon daigaku no
5.Altl^L/LH>1*ID9$V. ' Takeshi san juukyuusai
i'^x.X.t'A
X *A/X^x-x'yL/C
6.
i* -9 —
Suu san
suweedenjin
<75 -tt I -7 /It'- '*5' V ' (economics)
7. X — *5 Suu san no
senkoo
keezai
* if * t
8. u^^ h^5X> 4±X>C
Robaato san no senkoo h if *> t
tf i; fc i-
9 d/<—h*L/Xfa/C-th' Robaato san yonensee
6 if ab fc
10. c7/<—h*L/KLrp9v'-5*V
Robaato san nijuuissai
11. L A-tf/Cttv '/IXIA L A Yamashita sensee nihonjin
12. K>tLA4+A4+V'/A<7t Yamashita sensee Hawai daigaku
"""

is_english_word(text)