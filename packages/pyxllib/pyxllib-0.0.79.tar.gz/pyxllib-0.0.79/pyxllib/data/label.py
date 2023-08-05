#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : 陈坤泽
# @Email  : 877362867@qq.com
# @Date   : 2020/08/15 00:59

from tqdm import tqdm
from pyxllib.debug import *
from pyxllib.cv import *

__0_basic = """
"""


class BasicLabelData:
    """ 一张图一份标注文件的一些基本操作功能 """

    def __init__(self, root, data=None, *, fltr=None, slt=None, extdata=None):
        """
        :param root: 数据所在根目录
        :param data: [(file1, data1), (file2, data2), ...]
            如果未传入data具体值，则根据目录里的情况自动初始化获得data的值

            file是对应的File标注文件
            data1, data2 是读取的标注数据，根据不同情况，会存成不同格式
                如果是json则直接保存json内存对象结构
                如果是txt可能会进行一定的结构化解析存储
        :param extdata: 可以存储一些扩展信息内容
        :param fltr: filter的缩写，PathGroups 的过滤规则
            None，没有过滤规则，就算不存在slt格式的情况下，也会保留分组
            'json'等字符串规则, 使用 select_group_which_hassuffix，必须含有特定后缀的分组
            judge(k, v)，自定义函数规则
        :param slt: select的缩写，要选中的标注文件后缀格式
            如果传入slt参数，该 Basic 基础类只会预设好 file 参数，数据部分会置 None，需要后续主动读取
        """
        # 1 基础操作
        root = Dir(root)
        self.root, self.data, self.extdata = root, data or [], extdata

        if data is not None or slt is None:
            return

        # 2 如果没有默认data数据，以及传入slt参数，则需要使用默认文件关联方式读取标注
        data = []
        gs = PathGroups.groupby(Dir(root).select('**/*').subfiles())
        if isinstance(fltr, str):
            gs = gs.select_group_which_hassuffix(fltr)
        elif callable(fltr):
            gs = gs.select_group(fltr)

        for k in gs.data.keys():
            data.append((File(k, suffix=slt), None))

        self.data = data

    def __len__(self):
        return len(self.data)

    def writes(self, *, max_workers=8, prt=False):
        """ 重新写入每份标注文件

        可能是内存里修改了数据，需要重新覆盖
        也可能是从coco等其他格式初始化，转换而来的内存数据，需要生成对应的新标注文件
        """

        def write(x):
            file, data = x  # noqa
            if file:  # 如果文件存在，要遵循原有的编码规则
                with open(str(file), 'rb') as f:
                    bstr = f.read()
                encoding = get_encoding(bstr)
                file.write(data, encoding=encoding, if_exists='delete')
            else:  # 否则直接写入
                file.write(data)

        mtqdm(write, self.data, desc=f'{self.__class__.__name__}写入标注数据',
              max_workers=max_workers, disable=not prt)


__1_labelme = """
"""

# 我自己按照“红橙黄绿蓝靛紫”的顺序展示
LABEL_COLORMAP7 = [(0, 0, 0), (255, 0, 0), (255, 125, 0), (255, 255, 0),
                   (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255)]


def is_labelme_json_data(data):
    """ 是labelme的标注格式
    :param data: dict
    :return: True or False
    """
    has_keys = set('version flags shapes imagePath imageData imageHeight imageWidth'.split())
    return not (has_keys - data.keys())


def reduce_labelme_jsonfile(jsonpath):
    """ 删除imageData """
    p = str(jsonpath)

    with open(p, 'rb') as f:
        bstr = f.read()
    encoding = get_encoding(bstr)
    data = ujson.loads(bstr.decode(encoding=encoding))

    if is_labelme_json_data(data) and data['imageData']:
        data['imageData'] = None
        File(p).write(data, encoding=encoding, if_exists='delete')


class ToLabelmeJson:
    """ 标注格式转label形式

    初始化最好带有图片路径，能获得一些相关有用的信息
    然后自定义实现一个 get_data 接口，实现self.data的初始化，运行完可以从self.data取到字典数据
        根据需要可以定制自己的shape，修改get_shape函数
    可以调用write写入文件

    document: https://www.yuque.com/xlpr/pyxllib/ks5h4o
    """

    @deprecated(version=VERSION, reason='建议使用GenLabelme实现')
    def __init__(self, imgpath):
        """
        :param imgpath: 可选参数图片路径，强烈建议要输入，否则建立的label json会少掉图片宽高信息
        """
        self.imgpath = File(imgpath)
        # 读取图片数据，在一些转换规则比较复杂，有可能要用到原图数据
        if self.imgpath:
            # 一般都只需要获得尺寸，用pil读取即可，速度更快，不需要读取图片rgb数据
            self.img = PilImg(self.imgpath)
        else:
            self.img = None
        self.data = self.get_data_base()  # 存储json的字典数据

    def get_data(self, infile):
        """ 格式转换接口函数，继承的类需要自己实现这个方法

        :param infile: 待解析的标注数据
        """
        raise NotImplementedError('get_data方法必须在子类中实现')

    def get_data_base(self, name='', height=0, width=0):
        """ 获得一个labelme标注文件的框架 （这是标准结构，也可以自己修改定制）

        如果初始化时没有输入图片，也可以这里传入name等的值
        """
        # 1 默认属性，和图片名、尺寸
        if self.imgpath:
            name = self.imgpath.name
            height, width = self.img.size()
        # 2 构建结构框架
        data = {'version': '4.5.6',
                'flags': {},
                'shapes': [],
                'imagePath': name,
                'imageData': None,
                'imageWidth': width,
                'imageHeight': height,
                }
        return data

    def get_shape(self, label, points, shape_type=None, dtype=None, group_id=None, **kwargs):
        """最基本的添加形状功能

        :param shape_type: 会根据points的点数量，智能判断类型，默认一般是polygon
            其他需要自己指定的格式：line、circle
        :param dtype: 可以重置points的存储数值类型，一般是浮点数，可以转成整数更精简
        :param group_id: 本来是用来分组的，但其值会以括号的形式添加在label后面，可以在可视化中做一些特殊操作
        """
        # 1 优化点集数据格式
        points = np_array(points, dtype).reshape(-1, 2).tolist()
        # 2 判断形状类型
        if shape_type is None:
            m = len(points)
            if m == 1:
                shape_type = 'point'
            elif m == 2:
                shape_type = 'rectangle'
            elif m >= 3:
                shape_type = 'polygon'
            else:
                raise ValueError
        # 3 创建标注
        shape = {'flags': {},
                 'group_id': group_id,
                 'label': str(label),
                 'points': points,
                 'shape_type': shape_type}
        shape.update(kwargs)
        return shape

    def get_shape2(self, **kwargs):
        """ 完全使用字典的接口形式 """
        label = kwargs.get('label', '')
        points = kwargs['points']  # 这个是必须要有的字段
        kw = copy.deepcopy(kwargs)
        del kw['label']
        del kw['points']
        return self.get_shape(label, points, **kw)

    def add_shape(self, *args, **kwargs):
        self.data['shapes'].append(self.get_shape(*args, **kwargs))

    def add_shape2(self, **kwargs):
        self.data['shapes'].append(self.get_shape2(**kwargs))

    def write(self, dst=None, if_exists='delete'):
        """
        :param dst: 往dst目标路径存入json文件，默认名称在self.imgpath同目录的同名json文件
        :return: 写入后的文件路径
        """
        if dst is None and self.imgpath:
            dst = self.imgpath.with_suffix('.json')
        # 官方json支持indent=None的写法，但是ujson必须要显式写indent=0
        return File(dst).write(self.data, if_exists=if_exists, indent=0)

    @classmethod
    def create_json(cls, imgpath, annotation):
        """ 输入图片路径p，和对应的annotation标注数据（一般是对应目录下txt文件） """
        try:
            obj = cls(imgpath)
        except TypeError as e:  # 解析不了的输出错误日志
            get_xllog().exception(e)
            return
        obj.get_data(annotation)
        obj.write()  # 保存json文件到img对应目录下

    @classmethod
    def main_normal(cls, imdir, labeldir=None, label_file_suffix='.txt'):
        """ 封装更高层的接口，输入目录，直接标注目录下所有图片

        :param imdir: 图片路径
        :param labeldir: 标注数据路径，默认跟imdir同目录
        :return:
        """
        ims = Dir(imdir).select(['*.jpg', '*.png']).subfiles()
        if not labeldir: labeldir = imdir
        txts = [File(f.stem, labeldir, suffix=label_file_suffix) for f in ims]
        cls.main_pair(ims, txts)

    @classmethod
    def main_pair(cls, images, labels):
        """ 一一配对匹配处理 """
        Iterate(zip(images, labels)).run(lambda x: cls.create_json(x[0], x[1]),
                                         pinterval='20%', max_workers=8)


class Quad2Labelme(ToLabelmeJson):
    """ 四边形类标注转labelme """

    def get_data(self, infile):
        lines = File(infile).read().splitlines()
        for line in lines:
            # 一般是要改这里，每行数据的解析规则
            vals = line.split(',', maxsplit=8)
            if len(vals) < 9: continue
            pts = [int(v) for v in vals[:8]]  # 点集
            label = vals[-1]  # 标注的文本
            # get_shape还有shape_type形状参数可以设置
            #  如果是2个点的矩形，或者3个点以上的多边形，会自动判断，不用指定shape_type
            self.add_shape(label, pts)


class LabelmeData(BasicLabelData):
    @classmethod
    def gen_data(cls, imfile=None, **kwargs):
        """ 主要框架结构
        :param imfile: 可以传入一张图片路径
        """
        # 1 传入图片路径的初始化
        if imfile:
            file = File(imfile)
            name = file.name
            img = PilImg(str(file))
            height, width = img.size()
        else:
            name, height, width = '', 0, 0

        # 2 字段值
        data = {'version': '4.5.7',
                'flags': {},
                'shapes': [],
                'imagePath': name,
                'imageData': None,
                'imageWidth': width,
                'imageHeight': height,
                }
        if kwargs:
            data.update(kwargs)
        return data

    @classmethod
    def gen_shape(cls, label, points, shape_type=None, dtype=None, group_id=None, **kwargs):
        """ 最基本的添加形状功能

        :param shape_type: 会根据points的点数量，智能判断类型，默认一般是polygon
            其他需要自己指定的格式：line、circle
        :param dtype: 可以重置points的存储数值类型，一般是浮点数，可以转成整数更精简
        :param group_id: 本来是用来分组的，但其值会以括号的形式添加在label后面，可以在可视化中做一些特殊操作
        """
        # 1 优化点集数据格式
        points = np_array(points, dtype).reshape(-1, 2).tolist()
        # 2 判断形状类型
        if shape_type is None:
            m = len(points)
            if m == 1:
                shape_type = 'point'
            elif m == 2:
                shape_type = 'rectangle'
            elif m >= 3:
                shape_type = 'polygon'
            else:
                raise ValueError
        # 3 创建标注
        shape = {'flags': {},
                 'group_id': group_id,
                 'label': str(label),
                 'points': points,
                 'shape_type': shape_type}
        shape.update(kwargs)
        return shape

    @classmethod
    def gen_shape2(cls, **kwargs):
        """ 完全使用字典的接口形式 """
        label = kwargs.get('label', '')
        points = kwargs['points']  # 这个是必须要有的字段
        kw = copy.deepcopy(kwargs)
        del kw['label']
        del kw['points']
        return cls.gen_shape(label, points, **kw)

    def __init__(self, root, data=None, *, prt=False, fltr='json', slt='json', extdata=None):
        """
        :param root: 文件根目录
        :param data: [[jsonfile, lmdata], ...]，其中 lmdata 为一个labelme文件格式的标准内容
            如果未传入data具体值，则根据目录里的情况自动初始化获得data的值
        :param prt: 是否显示进度、中间运行信息
        """
        super().__init__(root, data, fltr=fltr, slt=slt, extdata=extdata)

        # 需要进一步读取数据，并过滤掉非labelme格式的json
        data = []
        for file, lmdata in tqdm(self.data, f'读取{self.__class__.__name__}数据', disable=not prt):
            lmdata = lmdata or file.read(mode='.json')
            if is_labelme_json_data(lmdata):
                data.append((file, lmdata))
        self.data = data

    def reduce(self):
        """ 移除imageData字段值 """
        for _, lmdata in self.data:
            lmdata['imageData'] = None

    def to_df(self, *, prt=True):
        """ 转成dataframe表格查看 """

        def read(x):
            file, lmdata = x
            if not lmdata['shapes']:
                return
            df = pd.DataFrame.from_records(lmdata['shapes'])
            df['filename'] = file.relpath(self.root)
            # 坐标转成整数，看起来比较精简点
            df['points'] = [np.array(v, dtype=int).tolist() for v in df['points']]
            ls.append(df)

        ls = []
        # 这个不建议开多线程，顺序会乱
        mtqdm(read, self.data, desc='labelme转df', disable=not prt)
        shapes_df = pd.concat(ls)
        # TODO flags 和 group_id 字段可以放到最后面
        shapes_df.reset_index(inplace=True, drop=True)

        return shapes_df

    @classmethod
    def init_from_coco(cls, root, gt_dict, *, prt=False):
        """
        :param root: 图片根目录
        :param gt_dict: coco格式的字典
            会将 ann json.dumps 为 str 存储为 label
            因为image标记方式的原因，如果在root找到多个匹配，会取第一匹配项
        :return:
            extdata，存储了一些匹配异常信息
        """
        root, data = Dir(root), []

        # 1 准备工作，构建文件名索引字典
        files = root.select('**/*').subfiles()
        gs = PathGroups.groupby(files)

        # 2 遍历生成labelme数据
        cd = CocoData(gt_dict)
        not_finds = set()  # coco里有的图片，root里没有找到
        multimatch = dict()  # coco里的某张图片，在root找到多个匹配文件
        for img, anns in cd.group_gt(reserve_empty=True):
            # 2.1 文件匹配
            imfiles = gs.find_files(img['file_name'])
            if not imfiles:  # 没有匹配图片的，不处理
                not_finds.add(img['file_name'])
                continue
            elif len(imfiles) > 1:
                multimatch[img['file_name']] = imfiles
                imfile = imfiles[0]
            else:
                imfile = imfiles[0]

            # 2.2 数据内容转换
            lmdata = LabelmeData.gen_data(imfile)
            lmdata['shapes'].append(LabelmeData.gen_shape(json.dumps(img, ensure_ascii=False), [[-10, 0], [-5, 0]]))
            for ann in anns:
                label = json.dumps(ann, ensure_ascii=False)
                points = xywh2ltrb(ann['bbox'])
                shape = LabelmeData.gen_shape(label, points)
                lmdata['shapes'].append(shape)
            data.append([imfile.with_suffix('.json'), lmdata])

        return cls(root, data,
                   extdata={'categories': cd.gt_dict['categories'],
                            'not_finds': not_finds,
                            'multimatch': Groups(multimatch)})

    def to_coco(self, categories=None, *, cat_id=None, outfile=None):
        """ 分两种大情况
        1、一种是raw原始数据转labelme标注后，首次转coco格式，这种编号等相关数据都可以重新生成
            raw_data --可视化--> labelme --转存--> coco
        2、还有种原来就是coco，转labelme修改标注后，又要再转回coco，这种应该尽量保存原始值
            coco --> labelme --手动修改--> labelme' --> coco'
        +、 1, 2两种情况是可以连在一起，然后形成 labelme 和 coco 之间的多次互转的

        :param categories: 类别
            默认只设一个类别 {'id': 0, 'name': 'text', 'supercategory'}
            支持自定义，所有annotations的category_id会取自定义cat的首项id值
        :param cat_id: 对于手动添加的普通labelme标注框，本来是没有类别的
            如果要转成coco，需要设置一个默认的类别id
            该默认值从categories第1项取
        :param outfile: 得到格式后直接转存为文件
        :return: gt_dict
            注意，如果对文件顺序、ann顺序有需求的，请先自行操作self.data数据后，再调用该to_coco函数
            对image_id、annotation_id有需求的，需要使用CocoData进一步操作
        """
        if not categories:
            categories = [{'id': 0, 'name': 'text', 'supercategory': ''}]
        cat_id = categories[0]['id'] if cat_id is None else cat_id
        ann_id = -1  # 新增的框box id为-1，然后每新增一个，递减1
        images, annotations = [], []

        for jsonfile, lmdata in self.data:
            img_id = -1
            for sp in lmdata['shapes']:
                d = json.loads(sp['label'])
                if isinstance(d, dict):
                    if sp['points'][0][0] < 0:  # 图像级标注
                        img_id = d['id']
                        images.append(d)
                    else:  # 普通框
                        annotations.append(d)
                else:
                    # 这种一般是手动新增的框
                    pts = [round(v, 2) for v in coords1d(sp['points'])]
                    ann = CocoGtData.gen_annotation(image_id=img_id, id=ann_id,
                                                    bbox=ltrb2xywh(pts),
                                                    label=sp['label'],
                                                    category_id=cat_id)
                    annotations.append(ann)
                    ann_id -= 1
        return CocoGtData.gen_data(images, annotations, categories, outfile)


__2_coco = """
"""


class CocoGtData:
    """ 需要同时绑定coco.json和图片目录，方便做些集成操作 """

    @classmethod
    def gen_image(cls, image_id, file_name, height, width, **kwargs):
        """ 初始化一个图片标注，使用位置参数，复用的时候可以节省代码量 """
        im = {'id': int(image_id), 'file_name': file_name,
              'height': int(height), 'width': int(width)}
        if kwargs:
            im.update(kwargs)
        return im

    @classmethod
    def gen_images(cls, imdir, start_idx=1):
        """ 自动生成标准的images字段

        :param imdir: 图片目录
        :param start_idx: 图片起始下标
        :return: list[dict(id, file_name, width, height)]
        """
        files = Dir(imdir).select(['*.jpg', '*.png']).subfiles()
        images = []
        for i, f in enumerate(files, start=start_idx):
            w, h = Image.open(str(f)).size
            images.append({'id': i, 'file_name': f.name, 'width': w, 'height': h})
        return images

    @classmethod
    def gen_annotation(cls, **kwargs):
        """ 智能地生成一个annotation字典

        这个略微有点过度封装了
        但没事，先放着，可以不拿出来用~~
        """
        a = kwargs.copy()

        # a = {'id': 0, 'area': 0, 'bbox': [0, 0, 0, 0],
        #       'category_id': 1, 'image_id': 0, 'iscrowd': 0, 'segmentation': []}

        if 'seg' in a:  # seg是一个特殊参数，使用一个多边形来标注
            if 'segmentation' not in a:
                a['segmentation'] = [a['seg']]
            del a['seg']
        if 'bbox' not in a:
            pts = []
            for seg in a['segmentation']:
                pts += seg
            a['bbox'] = ltrb2xywh(rect_bounds1d(pts))
        if 'area' not in a:  # 自动计算面积
            a['area'] = round(a['bbox'][2] * a['bbox'][3], 0)
        for k in ['id', 'image_id']:
            if k not in a:
                a[k] = 0
        if 'category_id' not in a:
            a['category_id'] = 1

        return a

    @classmethod
    def gen_quad_annotations(cls, file, *, image_id, start_box_id, category_id=1, **kwargs):
        """ 解析一张图片对应的txt标注文件

        :param file: 标注文件，有多行标注
            每行是x1,y1,x2,y2,x3,y3,x4,y4[,label] （label可以不存在）
        :param image_id: 该图片id
        :param start_box_id: box_id起始编号
        :param category_id: 归属类别
        """
        lines = File(file).read()
        box_id = start_box_id
        annotations = []
        for line in lines.splitlines():
            vals = line.split(',', maxsplit=8)
            if len(vals) < 2: continue
            attrs = {'id': box_id, 'image_id': image_id, 'category_id': category_id}
            if len(vals) == 9:
                attrs['label'] = vals[8]
            # print(vals)
            seg = [int(v) for v in vals[:8]]
            attrs['segmentation'] = [seg]
            attrs['bbox'] = ltrb2xywh(rect_bounds1d(seg))
            if kwargs:
                attrs.update(kwargs)
            annotations.append(cls.gen_annotation(**attrs))
            box_id += 1
        return annotations

    @classmethod
    def gen_categories(cls, cats):
        if isinstance(cats, list):
            # 如果输入是一个类别列表清单，则按1、2、3的顺序给其编号
            return [{'id': i, 'name': x, 'supercategory': ''} for i, x in enumerate(cats, start=1)]
        else:
            raise TypeError

        # TODO 扩展支持其他构造方法

    @classmethod
    def gen_data(cls, images, annotations, categories, outfile=None):
        data = {'images': images, 'annotations': annotations, 'categories': categories}
        if outfile is not None:
            File(outfile).write(data)
        return data


class CocoDtData:
    pass


class CocoData:
    """ 这个类可以封装一些需要gt和dt衔接的功能 """

    def __init__(self, gt, dt=None, *, min_score=0):
        """
        :param gt: gt的dict或文件
            gt是必须传入的，可以只传入gt
            有些任务理论上可以只有dt，但把配套的gt传入，能做更多事
        :param dt: dt的list或文件
        :param min_score: CocoMatch这个系列的类，初始化增加min_score参数，支持直接滤除dt低置信度的框
        """

        def get_dt_list(dt, min_score=0):
            # dt
            default_dt = []
            # default_dt = [{'image_id': self.gt_dict['images'][0]['id'],
            #                'category_id': self.gt_dict['categories'][0]['id'],
            #                'bbox': [0, 0, 1, 1],
            #                'score': 1}]
            # 这样直接填id有很大的风险，可能会报错。但是要正确填就需要gt的信息，传参麻烦~~
            # default_dt = [{'image_id': 1, 'category_id': 1, 'bbox': [0, 0, 1, 1], 'score': 1}]

            if not dt:
                dt_list = default_dt
            else:
                dt_list = dt if isinstance(dt, (list, tuple)) else File(dt).read()
                if min_score:
                    dt_list = [b for b in dt_list if (b['score'] >= min_score)]
                if not dt_list:
                    dt_list = default_dt
            return dt_list

        self.gt_dict = gt if isinstance(gt, dict) else File(gt).read()
        self.dt_list = get_dt_list(dt, min_score)

    @classmethod
    def is_gt_dict(cls, gt_dict):
        if isinstance(gt_dict, (tuple, list)):
            return False
        has_keys = set('images annotations categories'.split())
        return not (has_keys - gt_dict.keys())

    @classmethod
    def is_dt_list(cls, dt_list):
        if not isinstance(dt_list, (tuple, list)):
            return False
        item = dt_list[0]
        has_keys = set('score image_id category_id bbox'.split())
        return not (has_keys - item.keys())

    def clear_gt_segmentation(self, *, inplace=False):
        """ 有的coco json文件太大，如果只做普通的bbox检测任务，可以把segmentation的值删掉
        """
        gt_dict = self.gt_dict if inplace else copy.deepcopy(self.gt_dict)
        for an in gt_dict['annotations']:
            an['segmentation'] = []
        return gt_dict

    def select_gt(self, ids, *, inplace=False):
        """ 删除一些images标注（会删除对应的annotations），挑选数据，或者减小json大小

        :param ids: int类型表示保留的图片id，str类型表示保留的图片名，可以混合使用
            [341427, 'PMC4055390_00006.jpg', ...]
        :return: 筛选出的新字典
        """
        gt_dict = self.gt_dict
        # 1 ids 统一为int类型的id值
        if not isinstance(ids, (list, tuple, set)):
            ids = [ids]
        map_name2id = {item['file_name']: item['id'] for item in gt_dict['images']}
        ids = set([(map_name2id[x] if isinstance(x, str) else x) for x in ids])

        # 2 简化images和annotations
        dst = {'images': [x for x in gt_dict['images'] if (x['id'] in ids)],
               'annotations': [x for x in gt_dict['annotations'] if (x['image_id'] in ids)],
               'categories': gt_dict['categories']}
        if inplace: self.gt_dict = dst
        return dst

    def random_select_gt(self, number=20, *, inplace=False):
        """ 从gt中随机抽出number个数据 """
        ids = [x['id'] for x in self.gt_dict['images']]
        random.shuffle(ids)
        gt_dict = self.select_gt(ids[:number])
        if inplace: self.gt_dict = gt_dict
        return gt_dict

    def select_dt(self, ids, *, inplace=False):
        gt_dict, dt_list = self.gt_dict, self.dt_list
        # 1 ids 统一为int类型的id值
        if not isinstance(ids, (list, tuple, set)):
            ids = [ids]
        if gt_dict:
            map_name2id = {item['file_name']: item['id'] for item in gt_dict['images']}
            ids = [(map_name2id[x] if isinstance(x, str) else x) for x in ids]
        ids = set(ids)

        # 2 简化images
        dst = [x for x in dt_list if (x['image_id'] in ids)]
        if inplace: self.dt_list = dst
        return dst

    def select_gt_by_imdir(self, imdir, *, inplace=False):
        """ 基于imdir目录下的图片来过滤src_json """
        # 1 对比下差异
        json_images = set([x['file_name'] for x in self.gt_dict['images']])
        dir_images = set(os.listdir(str(imdir)))

        # df = SetCmper({'json_images': json_images, 'dir_images': dir_images}).intersection()
        # print('json_images intersection dir_images:')
        # print(df)

        # 2 精简json
        gt_dict = self.select_gt(json_images & dir_images)
        if inplace: self.gt_dict = gt_dict
        return gt_dict

    def _group_base(self, group_anns, reserve_empty=False):
        if reserve_empty:
            for im in self.gt_dict['images']:
                yield im, group_anns.get(im['id'], [])
        else:
            id2im = {im['id']: im for im in self.gt_dict['images']}
            for k, v in group_anns.items():
                yield id2im[k], v

    def group_gt(self, *, reserve_empty=False):
        """ 遍历gt的每一张图片的标注

        这个是用字典的方式来实现分组，没用 df.groupby 的功能

        :param reserve_empty: 是否保留空im对应的结果

        :return: [(im, annos), ...] 每一组是im标注和对应的一组annos标注
        """
        group_anns = defaultdict(list)
        [group_anns[an['image_id']].append(an) for an in self.gt_dict['annotations']]
        return self._group_base(group_anns, reserve_empty)

    def group_dt(self, *, reserve_empty=False):
        """ 对annos按image_id分组，如果有"""
        group_anns = defaultdict(list)
        [group_anns[an['image_id']].append(an) for an in self.dt_list]
        return self._group_base(group_anns, reserve_empty)

    def group_gt_dt(self, *, reserve_empty=False):
        """ 获得一张图片上gt和dt的标注结果

        [(im, gt_anns, dt_anns), ...]
        """
        raise NotImplementedError

    def reset_image_id(self, start=1, *, inplace=False):
        """ 按images顺序对图片重编号 """
        gt_dict = self.gt_dict if inplace else copy.deepcopy(self.gt_dict)
        # 1 重置 images 的 id
        old2new = {}
        for i, im in enumerate(gt_dict['images'], start=start):
            old2new[im['id']] = i
            im['id'] = i

        # 2 重置 annotations 的 id
        for anno in gt_dict['annotations']:
            anno['image_id'] = old2new[anno['image_id']]

        return gt_dict

    def reset_box_id(self, start=1, *, inplace=False):
        anns = self.gt_dict['annotations']
        if not inplace:
            anns = copy.deepcopy(anns)

        for i, anno in enumerate(anns, start=start):
            anno['id'] = i
        return anns

    def to_icdar_label_quad(self, outfile, *, min_score=0):
        """ 将coco的dt结果转为icdar的标注格式

        存成一个zip文件，zip里面每张图对应一个txt标注文件
        每个txt文件用quad八个数值代表一个标注框

        适用于 sroie 检测格式
        """
        from zipfile import ZipFile

        # 1 获取dt_list
        if min_score:
            dt_list = [b for b in self.dt_list if (b['score'] >= min_score)]
        else:
            dt_list = self.dt_list

        # 2 转df，按图片分组处理
        df = pd.DataFrame.from_dict(dt_list)  # noqa from_dict可以传入List[Dict]
        df = df.groupby('image_id')

        # 3 建立一个zip文件
        myzip = ZipFile(str(outfile), 'w')

        # 4 遍历每一组数据，生成一个文件放到zip里面
        id2name = {im['id']: pathlib.Path(im['file_name']).stem for im in self.gt_dict['images']}
        for image_id, items in df:
            label_file = id2name[image_id] + '.txt'
            quads = [rect2polygon(xywh2ltrb(x), dtype=int).reshape(-1) for x in items['bbox']]
            quads = [','.join(map(str, x)) for x in quads]
            myzip.writestr(label_file, '\n'.join(quads))
        myzip.close()

    def get_catname_func(self):
        id2name = {x['id']: x['name'] for x in self.gt_dict['categories']}

        def warpper(cat_id, default=...):
            """
            :param cat_id:
            :param default: 没匹配到的默认值
                ... 不是默认值，而是代表匹配不到直接报错
            :return:
            """
            if cat_id in id2name:
                return id2name[cat_id]
            else:
                if default is ...:
                    raise IndexError(f'{cat_id}')
                else:
                    return default

        return warpper
