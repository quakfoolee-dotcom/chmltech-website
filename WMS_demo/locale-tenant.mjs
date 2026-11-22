const rows=[
 ['Choose company','选择公司','選擇公司','Choisir une société'],
 ['Company members','公司成员','公司成員','Membres de la société'],
 ['Company','公司','公司','Société'],
 ['Current company','当前公司','目前公司','Société actuelle'],
 ['Loading companies…','正在加载公司…','正在載入公司…','Chargement des sociétés…'],
 ['No company access is available. Contact the beta administrator.','目前没有可访问的公司。请联系测试管理员。','目前沒有可存取的公司。請聯絡測試管理員。','Aucun accès à une société. Contactez l’administrateur bêta.'],
 ['You have unconfirmed changes. Resolve the pending save before switching companies.','您有尚未确认的更改。请先处理待确认保存，再切换公司。','您有尚未確認的變更。請先處理待確認儲存，再切換公司。','Des modifications restent non confirmées. Résolvez l’enregistrement avant de changer de société.'],
 ['Select a company explicitly to continue.','请明确选择公司后继续。','請明確選擇公司後繼續。','Sélectionnez explicitement une société pour continuer.'],
 ['Switch company','切换公司','切換公司','Changer de société'],
 ['Company access','公司访问权限','公司存取權限','Accès à la société'],
 ['Invited account ID','已邀请账户 ID','已邀請帳戶 ID','Identifiant du compte invité'],
 ['Remove company access','移除公司访问权限','移除公司存取權限','Retirer l’accès à la société'],
 ['I reviewed this company access change.','我已核查此公司权限更改。','我已核查此公司權限變更。','J’ai vérifié cette modification d’accès à la société.'],
 ['This changes access to this company only. It does not send an invitation.','这只更改当前公司的访问权限，不会发送邀请。','這只變更目前公司的存取權限，不會傳送邀請。','Cette action modifie uniquement l’accès à cette société et n’envoie aucune invitation.'],
 ['The company must retain at least one administrator.','公司必须保留至少一位管理员。','公司必須保留至少一位管理員。','La société doit conserver au moins un administrateur.'],
 ['Loading company members…','正在加载公司成员…','正在載入公司成員…','Chargement des membres de la société…'],
 ['No company members were returned.','没有返回公司成员。','未傳回公司成員。','Aucun membre de société retourné.'],
 ['Choose role','选择角色','選擇角色','Choisir un rôle'],
 ['Save company access','保存公司权限','儲存公司權限','Enregistrer l’accès à la société'],
 ['Enter an existing invited account ID.','请输入已邀请账户的有效 ID。','請輸入已邀請帳戶的有效 ID。','Saisissez l’identifiant valide d’un compte déjà invité.']
];
export const tenantCatalogue=Object.fromEntries(rows.map(([key,sc,tc,fr])=>[key,{'zh-Hans':sc,'zh-Hant':tc,fr}]));

