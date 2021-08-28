from wtforms import Form


class BaseForm(Form):
    def get_error(self):
        # err_str = ''
        # for value in self.errors.values():
        #     err_str += value[0]
        # return err_str

        err_str = list(self.errors.values())[0]
        return err_str
