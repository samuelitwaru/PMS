from django.conf import settings


def entity(request):
	return {
		"entity_name": settings.ENTITY_NAME,
		"entity_code": settings.ENTITY_CODE,
		"financial_year": settings.FINANCIAL_YEAR,
	}