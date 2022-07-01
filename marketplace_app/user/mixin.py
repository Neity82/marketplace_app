class ResponseDataMixin:
    @staticmethod
    def success_type_mapping(success: bool) -> str:
        """ Отдаем нужный тип ответа, исходя из переменной success """
        return "success" if success else "warning"

    def prepare_response_data(self, success: bool, message: str, **kwargs) -> dict:
        """Подготавливаем данные респонса для фронта"""
        response_type = self.success_type_mapping(success=success)
        response_data = {
            "type": response_type,
            "message": message,
        }
        for k, v in kwargs.items():
            response_data.update({k: v})
        return response_data

