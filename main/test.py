#encoding:utf-8
import datetime

class mark_type:
    checkdt=0
    annual=1
    expired=2
    lowstock=3
    urgepay=4

    def check(user):
        now = datetime.datetime.now()
        rs = QueryObj('''select whn from mark where type="{0}" and owner_id={1}'''.format(mark_type.checkdt,user.id))
        if len(rs):
            if rs[0].whn.day == now.day:
                return False
            delete("mark", obj(type=mark_type.annual,owner_id=user.id))
        insert("mark",obj(type=mark_type.checkdt, owner_id=user.id, whn=now))
        return True

class mark_驻地长:

    def update(user):
        if not check(user):
            return
        ar = QueryObj("select id from dev where checkdate between date('now','-30 day') and date('now')")
        ar = [obj(type=mark_type.annual, obj_id=x.id, owner_id=user.id, whn=now) for x in ar ]
        insert("mark",ar)
    def check(user):
        return querycount( "mark", obj(type=mark_type.annual, owner_id=user.id))
    def read(obj_id):
        delete("mark", obj(type=mark_type.annual, owner_id=user.id,obj_id=obj_id))
