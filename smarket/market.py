"""
SAVE CODE:

M.save=function()
	{
		//output cannot use ",", ";" or "|"
		var str=''+
		parseInt(M.officeLevel)+':'+
		parseInt(M.brokers)+':'+
		parseInt(M.graphLines)+':'+
		parseFloat(M.profit)+':'+
		parseInt(M.graphCols)+':'+
		' ';
		for (var iG=0;iG<M.goodsById.length;iG++)
		{
			var it=M.goodsById[iG];
			str+=parseInt(it.val*100)+':'+parseInt(it.mode)+':'+parseInt(it.d*100)+':'+parseInt(it.dur)+':'+parseInt(it.stock)+':'+parseInt(it.hidden?1:0)+':'+parseInt(it.last)+'!';
		}
		str+=' '+parseInt(M.parent.onMinigame?'1':'0');
		return str;
	}
"""

# SAMPLE:
# 0:0:1:-5.526190275271631:1: 1175:0:-4:430:0:0:0!430:4:-67:10:0:0:0!950:4:-107:212:0:0:0!723:2:-64:122:0:0:0!825:4:-115:24:0:0:0!3565:2:-42:508:0:0:0!1046:4:-178:21:0:0:0!4899:2:-60:191:0:0:0!10123:1:22:507:0:0:0!974:4:-179:265:0:0:0!1454:4:-213:356:0:1:0!4527:4:-170:129:0:1:0!12615:5:3:89:0:1:0!5335:4:-155:654:0:1:0!12621:2:-53:288:0:1:0!13707:5:-57:260:0:1:0! 0
