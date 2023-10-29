
    Проверяет допустимость символов.
    """
    def __call__(self, form, field):
        if self.message is None:
            self.message = f'Some element of {field.data} not in {self.values}'
        symbols_validation(field.data, validators.ValidationError(self.message))