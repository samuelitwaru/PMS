from django.conf import settings


def entity(request):
	return {
		"entity_name": settings.ENTITY_NAME,
		"entity_code": settings.ENTITY_CODE,
		"FY": settings.FINANCIAL_YEAR,
		"FY_start": settings.FY_START_DATE,
		"FY_stop": settings.FY_STOP_DATE,
	}