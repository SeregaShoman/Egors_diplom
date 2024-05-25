from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from configs import CONFIG
from dependencies import get_db_session, decode_token


static_tags_router = APIRouter(
    tags=["Роутер который вернёт статические данные о ТЭГАХ"],
    prefix="/tags",
    default_response_class=ORJSONResponse
)


@static_tags_router.get(
    path="/", status_code=status.HTTP_200_OK
)
async def get_static_tags():
    return {
        "patners_services":{
            "Banking": "Банковское дело",
            "IT": "IT",
            "Law and Jurisprudence": "Право и юриспруденция",
            "Hospitality and Service": "Гостеприимство и сервис",
            "Commerce": "Коммерция",
            "Internships and Practicums": "Практики и стажировки",
            "Mentors": "Наставники",
            "Vacancies and Employment": "Вакансии и трудоустройство",
        },
        "studing_proccess":{
            "Sports": "Спорт",
            "Creativity": "Творчество",
            "Media/Journalism": "СМИ/Медиа",
            "Additional Education": "Дополнительное образование"
        }
    }