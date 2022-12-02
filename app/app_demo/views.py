from flask import render_template, redirect, url_for, flash, request
from app.app_demo import demo_bp
from .models import *
from app.app_account.models import User
from .forms import TableActForm, DeleteForm, ContentForm
from app import db

import app.utils.wutongchain as wtc
import app.utils.myvessel as mvsl

global status
status = 0

demolinks = [
    ['Hello 梧桐链！', 'hello'],
    ['用户信息', 'userinfo'],
    ["地图", "map"],
    ["碳排放", "carbon"],
    ["碳交易", "carbon_transaction"],
    ]

@demo_bp.route('/test/<demoname>', methods=['GET','POST'])
def demotest(demoname):

    # 示例: 与梧桐链数据交互
    if demoname == "hello":
        return HelloWTC()
    # 示例: 读取本地数据库（用户信息）
    elif demoname == 'userinfo':       
        return TableUserInfo()
    elif demoname == 'map':       
        return redirect(url_for('map.hello_map'))
    elif demoname == 'carbon':
        return redirect(url_for('carbon.carbon_BaseInfo'))
    elif demoname == 'carbon_transaction':
        return redirect(url_for('carbon.carbon_Transaction'))
    else:
        return redirect(url_for('account.panel'))
    

# 与梧桐链数据交互
def HelloWTC():
    port_list = {
        "洋山港": "CNYSN",
        "烟台港": "CNYAN",
    }
    # info_yangshan = 

    text_list = ["Hello Hello Hi Hi Hi",
        f"区块浏览器: {wtc.get_browser_url()}",
        f"应用链: {wtc.get_ledger_name()}",
        f"当前区块高度: {wtc.get_block_height()}",
        f"洋山港: {mvsl.get_port_by_code(port_list['洋山港'])}",
        f"烟台港: {mvsl.get_port_by_code(port_list['烟台港'])}",
        ]

    return render_template(
        "helloWTC.html",
        title = 'Hello 梧桐链',
        demolinks = demolinks,
        text_list = text_list,
    )


# 读取 User 表的数据
def TableUserInfo():
  
    form = TableActForm()       # 表格form
    delete_form = DeleteForm()  # 删除记录form
    delete_no = delete_form.number.data
    add_forms = []  # 添加记录
    atbs = []       # 属性（列）
    recs = []       # 记录（行）

    tabletitle = '用户信息'
    # atbs = ['user_id','username']
    atbs = ["", "账号", "用户名"]
    results = User.query.all()  # 获取 User 表全部记录
    row_id = 1
    # 读 User 表的记录
    for res in results:
        recs.append([row_id, res.user_id, res.username])
        row_id += 1

    # atb[0]是id
    for atb in atbs[1:]:
        content = ContentForm()
        add_forms.append(content)

    # 表的增删改
    global status
    delete_no = delete_form.number.data
    if form.validate_on_submit():
        if form.add.data:
            status = 1
        elif form.delete.data:
            status = 2
        elif form.save.data:
            '''
            if('status' in globals().keys()):
                s1 = "status = " + str(status)
                flash(s1)
            else:
                flash('未找到status')
            '''
            status = 3
            db.session.commit()
            # flash('保存更改！')
        elif form.restore.data:
            status = 4
            db.session.rollback()
            # flash('撤销更改！')

    if delete_no != None:
        # flash(str(delete_no))
        cnt = 1
        for res in results:
            if cnt != delete_no:
                cnt = cnt + 1
            else:
                db.session.delete(res)
                db.session.commit()
                recs[delete_no-1][0] = '!!!'
                break

    return render_template(
        "tables.html",
        title = '用户信息',
        demolinks = demolinks,
        tabletitle = tabletitle,
        atbs = atbs,
        recs = recs,
        form = form,
        delete_form = delete_form,
        add_forms = add_forms,
        status = status
    )
