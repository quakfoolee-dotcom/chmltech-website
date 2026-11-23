// Shared browser permissions for the existing read-only cloud connector.
export const cloudQBOActionAllowed=(name,role,isDemo)=>!isDemo&&['cloud-qbo-view','cloud-qbo-configure','cloud-qbo-connect','cloud-qbo-disconnect','cloud-qbo-refresh','cloud-qbo-compare'].includes(name)&&(role==='Admin'||role==='Accounting'&&['cloud-qbo-view','cloud-qbo-refresh','cloud-qbo-compare'].includes(name));
