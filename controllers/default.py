# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict(message=T('Welcome to web2py!'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


def browseandshop():
    session.cart=[]
    if request.vars:
        session.cart.append(request.vars)
        response.flash(request.vars);
    category_list=db(db.category_type.id>0).select().as_list()
    style_list=db(db.style_type.id>0).select().as_list()
    shape_list=db(db.shape_type.id>0).select().as_list()
    size_list=db(db.size_type.id>0).select().as_list()
    price_group_list=db(db.price_group_type.id>0).select().as_list()
    product_list=db(db.product.id>0).select(db.product.id,db.product.p_name,db.product.p_image,db.product.p_price).as_list()
    return locals()

@auth.requires_login()
#To maintain cart across session
def maintain_cart():
    key=str(request.args(0))
    if not session.cart:
        session.cart={}
        #response.flash="Found Empty Cart"
    if key in session.cart:
        del session.cart[key]
    else:
        session.cart[key]=1

@auth.requires_login()
#To see and process the cart
def yourcart():
    if not session.cart:
        session.flash = 'Add something to cart'
        redirect(URL('default', 'browseandshop'))
    else:
        product_list=[]
        for i in session.cart:
            for row in db(db.product.id==int(i)).select(db.product.id,db.product.p_name,db.product.p_image,db.product.p_price):
                product_list.append(row)
        return locals()
