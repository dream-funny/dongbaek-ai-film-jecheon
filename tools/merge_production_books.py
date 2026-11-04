"""두 제작 통합문서의 시트와 이미지를 하나로 합친다. 원본은 유지한다."""
from pathlib import Path
from copy import copy,deepcopy
from io import BytesIO
from openpyxl import Workbook,load_workbook
from openpyxl.drawing.image import Image
ROOT=Path(__file__).resolve().parent.parent
sources=[('DONGBAEK_PRODUCTION_LISTS.xlsx',{}),('DONGBAEK_CHARACTER_BOOK.xlsx',{'인물 리스트':'5_캐릭터설명','C01_나':'6_나_캐릭터시트','C02_점순이':'7_점순이_캐릭터시트','C03_나의 어머니':'8_어머니_캐릭터시트'})]
out=Workbook();out.remove(out.active)
expected=[];images=0
for filename,names in sources:
 book=load_workbook(ROOT/filename)
 for src in book:
  dst=out.create_sheet(names.get(src.title,src.title))
  for row in src:
   for cell in row:
    c=dst.cell(cell.row,cell.column,cell.value)
    if cell.has_style:
     for attr in ['font','fill','border','alignment','protection']:setattr(c,attr,copy(getattr(cell,attr)))
     c.number_format=cell.number_format
    if cell.hyperlink:c.hyperlink=copy(cell.hyperlink)
    if cell.comment:c.comment=copy(cell.comment)
  for key,dim in src.row_dimensions.items():dst.row_dimensions[key]=copy(dim)
  for key,dim in src.column_dimensions.items():dst.column_dimensions[key]=copy(dim)
  for span in src.merged_cells.ranges:dst.merge_cells(str(span))
  dst.sheet_format=copy(src.sheet_format)
  dst.sheet_properties=deepcopy(src.sheet_properties)
  dst.views=deepcopy(src.views)
  dst.freeze_panes=src.freeze_panes
  dst.auto_filter=deepcopy(src.auto_filter)
  dst.page_margins=copy(src.page_margins)
  dst.page_setup=copy(src.page_setup)
  dst.print_options=copy(src.print_options)
  dst.print_title_rows=src.print_title_rows
  dst.print_title_cols=src.print_title_cols
  if src.print_area:dst.print_area=str(src.print_area).split('!',1)[-1]
  for old in src._images:
   im=Image(BytesIO(old._data()));im.width=old.width;im.height=old.height
   dst.add_image(im,deepcopy(old.anchor));images+=1
  expected.append((dst.title,src.max_row,src.max_column,[[c.value for c in row] for row in src]))
path=ROOT/'DONGBAEK_PRODUCTION_MASTER.xlsx';out.save(path)
check=load_workbook(path)
assert len(check.sheetnames)==9
assert sum(len(s._images) for s in check)==images==7
for name,nrows,ncols,values in expected:
 s=check[name]
 assert (s.max_row,s.max_column)==(nrows,ncols)
 assert [[c.value for c in row] for row in s]==values
assert sum(check['1_씬리스트'].cell(r,8).value for r in range(2,12))==240
print('검증 완료: 9개 시트 / 원본 셀 내용 일치 / 이미지 7개 / 10씬·240초')
print(path)
