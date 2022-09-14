import logging
from vuejs_api import doc
type = input('输入要进行的操作(menu,image,check,pdf):')
if type=='menu':
    doc.Doc2Pdf().menu_tree_2_json().quit()
elif type=='image':
    # 截取图片
    doc.Doc2Pdf.multi_thread_generate_with_pool()
    pass
elif type=='check':
    doc.MenuTree().check_images()
    pass
elif type=='pdf':
    pass
else:
    logging.exception('未知的类型')

# vue_turorial.multi_thread_generate()
# vue_turorial.check_images()
# vue_turorial.VueTurorialDoc2Pdf.image_list_2_pdf_by_pillow()