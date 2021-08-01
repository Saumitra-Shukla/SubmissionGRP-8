from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView
from newspapers.models import Preference,Newspaper_name,News
from django.core.mail import send_mail
from django.conf import settings
import json
class TestPage(TemplateView):
    template_name = 'test.html'

def main(request):
	return render_to_response('main.html', {}, context_instance=RequestContext(request))







import tracemalloc
from django.http import JsonResponse
#from rest_framework import status
#from rest_framework.response import Response
import os
from  datetime import datetime
started_pids=[]


def take_snap(request):
	global started_pids
	current_pid= os.getpid()
	if current_pid not in started_pids:
		tracemalloc.start()
		started_pids.append(current_pid)

		# taking initial snapshot
		init_snap = tracemalloc.take_snapshot()
		# storing the pid of process to compare if same process are running or not
		init_snap.pid = current_pid

		# storing initial snap to 0th index, current snap to index 1
		#s = [init_snap, init_snap]


		# dumping initial snapshot
		init_snap.dump("init_snap"+str(current_pid)+".log")

		# TODO : send snap details in Response obj

		snap_details = [current_pid]
		return JsonResponse({"data":snap_details},status=200)

	else:
		
			# taking new snapshot
		new_snap = tracemalloc.take_snapshot()
		new_snap.pid = current_pid

		init_snap = tracemalloc.Snapshot.load("init_snap"+str(current_pid)+".log")

		# comparing current snapshot to initial
		top_stats = new_snap.compare_to(init_snap, "lineno")
		new_snap.stats_init = top_stats

		# comparing current snapshot to prev snap
		# top_stats = new_snap.compare_to(s[1], "lineno")
		# new_snap.stats_prev = top_stats


		hour = str(datetime.now().time().hour)
		mins = str(datetime.now().time().minute)
		sec = str(datetime.now().time().second)
		new_snap.dump("curr_snap"+str(current_pid)+hour+mins+sec+".log")
		#s[1] = new_snap
		try:
			# TODO: return diff in stats to cron
			curr_output = [current_pid]

			for stats in new_snap.stats_init[:15]:
				curr_output.append(str(stats))

			# curr_output.append("</br><br><p>is it same as prev_snap_pid = " + str(new_snap.is_prev_pid_same) + "</br>")
			# curr_output.append("<p>Spikes compared to prev snapshot :</p></br>")
			# for stats in new_snap.stats_prev[:15]:
			# 	curr_output.append("<li>" + str(stats) + "</li></br>")

			return JsonResponse({"data":curr_output},status=200)
		except Exception as e:
			return JsonResponse({"data":[str(e)]},status=200)


from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def stop_trace(request):
	print(request.POST)
	pid = request.POST.get("pid")
	if int(pid) == int(str(os.getpid())):
		tracemalloc.stop()
		started_pids.remove(pid)
		return JsonResponse({"data":"True"},status=200)
	return JsonResponse({"data":"False"}, status=200)














def email(request):

    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['abhi95103@gmail.com',]

    send_mail( subject, message, email_from, recipient_list )

    return redirect('redirect to a new page')
