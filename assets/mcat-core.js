(function(root){
 const DAY=86400000;
 function key(date=new Date()){const parts=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(date);const part=t=>parts.find(p=>p.type===t).value;return `${part('year')}-${part('month')}-${part('day')}`;}
 const shift=(s,n)=>new Date(Date.parse(s+'T12:00:00Z')+n*DAY).toISOString().slice(0,10);
 function stats(entries,today=key()){
 const totals={};for(const e of entries)totals[e.date]=(totals[e.date]||0)+e.minutes;
 const d=new Date(today+'T12:00:00Z'),weekday=(d.getUTCDay()+6)%7,weekStart=shift(today,-weekday),monthStart=today.slice(0,8)+'01';
 const sum=start=>Object.entries(totals).filter(([date])=>date>=start&&date<=today).reduce((n,[,v])=>n+v,0);
 let streak=0,cursor=totals[today]?today:shift(today,-1);while(totals[cursor]>0){streak++;cursor=shift(cursor,-1);}
 const daily=totals[today]||0,yesterday=totals[shift(today,-1)]||0,weekly=sum(weekStart),monthly=sum(monthStart);
 return {today,yesterdayDate:shift(today,-1),daily,yesterday,weekly,monthly,weeklyAverage:weekly/(weekday+1),monthlyAverage:monthly/Number(today.slice(-2)),weekStart,monthStart,totals,streak,best:Math.max(0,...Object.values(totals)),allTime:entries.reduce((n,e)=>n+e.minutes,0),daysLeft:Math.round((Date.parse('2027-03-19T12:00:00Z')-Date.parse(today+'T12:00:00Z'))/DAY)};
 }
 root.McatStats={key,shift,stats};
})(typeof window==='undefined'?globalThis:window);
