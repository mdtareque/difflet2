# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    redirect(URL('default', 'search'))
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def search():
    recent_searches = {}
    entities =  { }
    categories = []
    for c in categories:
        es = db(db.entity.category == c['id']).select(db.entity.name)
        entities[c['name']] = []
        for e in es:
            entities[c['name']].append(e['name'])
    return locals()

def saveSearch(e1, e2):
    # save to recents
    return


def difflet():
    e1, e2 = request.vars['e1'],request.vars['e2']
    e1, e2 = e1.lower(), e2.lower()
    saveSearch(e1, e2)
    #e1id=(db(db.thing.name==e1).select())[0]['id']
    #e2id=(db(db.thing.name==e2).select())[0]['id']

    q1 = (db.listings.thing == db.thing.id) & (db.listings.point == db.point.id) & (db.listings.description == db.description.id) & (db.thing.name == e1)
    q2 = (db.listings.thing == db.thing.id) & (db.listings.point == db.point.id) & (db.listings.description == db.description.id) & (db.thing.name == e2)
    
    e1rows = db(q1).select(db.point.property, db.description.body, db.point.id)
    e2rows = db(q2).select(db.point.property, db.description.body, db.point.id)
    #e2rows = db(db.listing.entity==e2id).select(join = db.diff_point.on(db.listing.diff_point == db.diff_point.id))

    e1_dp_id = []
    for i in range(0, len(e1rows)):
        e1_dp_id.append(e1rows[i]['point']['id'])
        #e1_dp_id.append(e1rows[i]['diff_point.id'] )
    e2_dp_id = []
    for i in range(0, len(e2rows)):
        e2_dp_id.append(e2rows[i]['point']['id'])
        #e2_dp_id.append(e2rows[i]['diff_point.id'] )

    # {  diff_point : (e1, e2)}
    common=[]
    for i in e1_dp_id:
        if i in e2_dp_id:
            common.append(i)

    output={}

    for r in e1rows:
        if r['point']['id'] in common:
            output[r['point']['property']] = (r['description']['body'] , '')

    for r in e2rows:
        if r['point']['id'] in common:
            old_tuple = output[r['point']['property']]
            output[r['point']['property']] = (old_tuple[0], r['description']['body'])
#        if r['diff_point.id'] in common:
#            old_tuple = output[r['diff_point.name']]
#            output[r['diff_point.name']] =  ( old_tuple[0],  r['listing.summary'])

    return locals()


def create():
    e = request.args[0]
    if e == 'category':
        category = SQLFORM(db.category).process()
    if e == 'thing':
        thing = SQLFORM(db.thing).process()
    if e == 'point':
        point = SQLFORM(db.point).process()
    if e == 'description':
        description = SQLFORM(db.description).process()
    if e == 'listing':
        listing = SQLFORM(db.listings).process()
    if e == 'recent':
        recent = SQLFORM(db.recents).process()
    if e == 'popular':
        popular = SQLFORM(db.popular).process()
    return locals()

def managething():
    thing = SQLFORM.smartgrid(db.thing)
    return locals()

def manage():
    e = request.args(0)
    if e == 'category' or e is None:
        #category = SQLFORM.grid(db.category)
        category = SQLFORM.smartgrid(db.category)
    if e == 'thing' or e is None:
        thing = SQLFORM.smartgrid(db.thing)
    if e == 'point' or e is None:
        point = SQLFORM.smartgrid(db.point)
    if e == 'description' or e is None:
        description = SQLFORM.smartgrid(db.description)
    if e == 'listing' or e is None:
        listing = SQLFORM.smartgrid(db.listings)
    if e == 'recent' or e is None:
        recent = SQLFORM.smartgrid(db.recents)
    if e == 'popular' or e is None:
        popular = SQLFORM.smartgrid(db.popular)
    return locals()


def template():
    response.view = 'default/difflet_template.html'
    return locals()




def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """]
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename
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
