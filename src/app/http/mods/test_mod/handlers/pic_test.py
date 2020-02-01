from app.http.handler_base import HandlerBase


class pic_test(HandlerBase):
    def post(self):
        pic_body = self.get_files('pic')
        # print(pic)

        open('pics/example.jpg', 'wb').write(pic_body)

        self.send_ok({})
        return
