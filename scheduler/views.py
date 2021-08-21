from django.http import request, JsonResponse
from scheduler.management.commands._v1private import get_cases_data, get_state_codes, get_vaccination_data
import pandas

def runTests(request):
    context = {}
    try:
        cases  = get_cases_data()
        assert(isinstance(cases, pandas.core.frame.DataFrame))
    except Exception as err:
        context['cases_err'] = err.__str__()
    else:
        context['cases_err'] = None
    
    try:
        vacc  = get_vaccination_data()
        assert(isinstance(vacc, pandas.core.frame.DataFrame))
    except Exception as err:
        context['vacc_err'] = err.__str__()
    else:
        context['vacc_err'] = None

    try:
        codes  = get_state_codes()
        assert(isinstance(codes, pandas.core.frame.DataFrame))
    except Exception as err:
        context['codes_err'] = err.__str__()
    else:
        context['codes_err'] = None
    
    return JsonResponse(context)
