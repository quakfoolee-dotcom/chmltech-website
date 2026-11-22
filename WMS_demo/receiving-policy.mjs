export const receivingCommands=['receiving:bin','receiving:createInspection','receiving:submitInspection','receiving:approveInspection','receiving:cancelInspection','receiving:createTask','receiving:finishTask','receiving:cancelTask','receiving:loadDemo'];
const warehouse=['receiving:createInspection','receiving:submitInspection','receiving:createTask','receiving:finishTask','receiving:cancelTask'];
export const receivingRoleAllowed=(command,role)=>receivingCommands.includes(command)&&(role==='Admin'||role==='Warehouse'&&warehouse.includes(command));
export const receivingActionCommands=Object.fromEntries(receivingCommands.map(c=>['rcv-'+c.slice(10),[c]]));

