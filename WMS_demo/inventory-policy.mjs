import {receivingCommands,receivingRoleAllowed,receivingActionCommands} from './receiving-policy.mjs?demo=9c44c6dabb8d4728';
// Command policy shared by the browser, HTTP service and SQL-policy tests.
// No engine imports: cloud cold starts must remain acyclic.
export const inventoryRoles={
 Admin:['saveCustom','createItem','saveItemText','setTracking','receiveStock','moveStock','countStock','scrapStock','setCost','units:save','units:active','business:profile','business:replenishment','business:reorder','business:approveReorder','business:cancelReorder','business:transfer','business:shipTransfer','business:receiveTransfer','business:cancelTransfer','business:scan','business:finishScannedPick','count:create','count:record','count:submit','count:recount','count:cancel','count:approve','cost:enableFIFO','transferCost:allocate'],
 Warehouse:['receiveStock','moveStock','countStock','scrapStock','business:transfer','business:shipTransfer','business:receiveTransfer','business:cancelTransfer','business:scan','business:finishScannedPick','count:create','count:record','count:submit','count:recount','count:cancel'],
 Purchasing:['units:save','units:active','business:profile','business:replenishment','business:reorder','business:approveReorder','business:cancelReorder'],
 Accounting:['setCost','cost:enableFIFO','transferCost:allocate']
};
for(const role of ['Admin','Warehouse'])inventoryRoles[role].push(...receivingCommands.filter(c=>receivingRoleAllowed(c,role)));
export const inventoryCommands=inventoryRoles.Admin;
export const inventoryRoleAllowed=(command,role)=>inventoryRoles[role]?.includes(command)===true;
export const inventoryActionCommands={
 'edit-custom':['saveCustom'],'edit-item':['saveItemText'],'new-item':['createItem'],'receive':['receiveStock'],'move':['moveStock'],'count':['countStock'],'scrap':['scrapStock'],'lot-info':['setTracking'],'set-cost':['setCost'],
 'biz-profile':['business:profile'],'biz-unitNew':['units:save'],'biz-unitEdit':['units:save'],'biz-unitStatus':['units:active'],
 'biz-replenishment':['business:replenishment'],'biz-reorder':['business:reorder'],'biz-approveReorder':['business:approveReorder'],'biz-cancelReorder':['business:cancelReorder'],
 'biz-transfer':['business:transfer'],'biz-shipTransfer':['business:shipTransfer'],'biz-receiveTransfer':['business:receiveTransfer'],'biz-cancelTransfer':['business:cancelTransfer'],
 'biz-scanReceive':['business:scan'],'biz-scanPick':['business:scan'],'biz-scanCount':['business:scan'],'biz-finishScannedPick':['business:finishScannedPick'],
 'ins-create':['count:create'],'ins-entry':['count:record'],'ins-submit':['count:submit'],'ins-recount':['count:recount'],'ins-cancel':['count:cancel'],'ins-approve':['count:approve'],
 'value-enable':['cost:enableFIFO'],'delivery-freight':['transferCost:allocate']
};

Object.assign(inventoryActionCommands,receivingActionCommands);


