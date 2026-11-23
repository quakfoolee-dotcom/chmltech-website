// Calendar defaults and current-day decisions only. Persisted timestamps remain
// instants; saved YYYY-MM-DD values are calendar dates and are never shifted.
const formatters=new Map();
export function businessDay(state,now=new Date()){
 if(typeof now==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(now))return now;
 const instant=new Date(now),timezone=state?.organization?.timezone;
 if(!timezone)return instant.toISOString().slice(0,10);
 let formatter=formatters.get(timezone);if(!formatter){formatter=new Intl.DateTimeFormat('en-US',{timeZone:timezone,year:'numeric',month:'2-digit',day:'2-digit'});formatters.set(timezone,formatter);}
 const parts=Object.fromEntries(formatter.formatToParts(instant).filter(p=>['year','month','day'].includes(p.type)).map(p=>[p.type,p.value]));return parts.year.padStart(4,'0')+'-'+parts.month+'-'+parts.day;
}
