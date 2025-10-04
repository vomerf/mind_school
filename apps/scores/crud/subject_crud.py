from apps.base_crud import CRUDBase
from apps.scores.models import Subject


class SubjectCRUD(CRUDBase): ...


subject_crud = SubjectCRUD(Subject)
