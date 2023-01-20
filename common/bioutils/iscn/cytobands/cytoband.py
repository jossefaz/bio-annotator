import enum
from typing import Union

'''
Javascript code used to extract cytobands from USCS browser
const a = document.getElementsByName('ideoMap')
let my_list = []
for (let cytoband of a[0].children) {
    let splitted = cytoband.title.split(' ')
    let cytobandType = splitted[0][0]
    let bands = splitted[0].split(`${cytobandType}`)[1]
    let band = bands[0]
    let sub_band = bands[1]
    let sub_sub_band = bands.split('.').length > 1 && bands.split('.')[1]
    let [range_start, range_end] = splitted[1].split(':')[1].split('-')
    my_list.push(`Cytoband(CytobandTypeEnum.${cytobandType}, range(${range_start}, ${range_end}), ${band}, ${sub_band}${sub_sub_band ? ',' + sub_sub_band: ''})`)
}
copy(my_list)
'''



class CytobandTypeEnum(enum.Enum):
    p = 'p'
    q = 'q'


class Cytoband:

    def __init__(self, type: CytobandTypeEnum, range: range, band: int, s_band: int, ss_band: int = None):
        self.type = type
        self.range = range
        self.band = band
        self.s_band = s_band
        self.ss_band = ss_band

    @property
    def cytoband(self):
        return f"{self.type.value}{self.band}{self.s_band}{f'.{self.ss_band}' if self.ss_band else ''}"

    def __contains__(self, position: Union[int, range]):
        if isinstance(position, range):
            return bool(range(max(position[0], self.range[0]), min(position[-1], self.range[-1]) + 1))
        if not isinstance(position, int):
            return False
        return position in self.range

