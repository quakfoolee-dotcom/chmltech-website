const rows=[
['The save request is too large. Reduce the CSV rows or inspection photos before saving.','保存请求过大。请减少 CSV 行数或检查照片后再保存。','儲存請求過大。請減少 CSV 列數或檢查照片後再儲存。','La demande est trop volumineuse. Réduisez les lignes CSV ou les photos de contrôle avant d’enregistrer.'],
 ['Use a JSON object request.','请求必须为 JSON 对象。','請求必須為 JSON 物件。','La requête doit être un objet JSON.'],
 ['Invalid JSON request.','JSON 请求无效。','JSON 請求無效。','Requête JSON non valide.'],
 ['Request too large.','请求内容过大。','請求內容過大。','Requête trop volumineuse.'],
 ['Enter your email and password.','请输入邮箱和密码。','請輸入電子郵件與密碼。','Saisissez votre adresse courriel et votre mot de passe.'],
 ['Authentication is temporarily unavailable. Try again shortly.','登录服务暂时不可用，请稍后重试。','登入服務暫時無法使用，請稍後再試。','Le service de connexion est temporairement indisponible. Réessayez dans un instant.'],
 ['Wait a minute before trying again.','请稍等一分钟后再试。','請稍候一分鐘再試。','Patientez une minute avant de réessayer.']
 ,['Sign-in protection is not configured.','登录保护尚未配置。','登入保護尚未設定。','La protection de connexion n’est pas configurée.']
 ,['Too many sign-in attempts. Try again later.','登录尝试次数过多，请稍后重试。','登入嘗試次數過多，請稍後再試。','Trop de tentatives de connexion. Réessayez plus tard.']
 ,['The beta service is temporarily unavailable. Try again shortly.','测试版服务暂时不可用，请稍后重试。','測試版服務暫時無法使用，請稍後再試。','Le service bêta est temporairement indisponible. Réessayez dans un instant.']
 ,['Cloud access is not configured.','云端访问尚未配置。','雲端存取尚未設定。','L’accès au service infonuagique n’est pas configuré.']
 ,['Use the approved Harbor page to submit changes.','请从已批准的 Harbor 页面提交更改。','請從已核准的 Harbor 頁面提交變更。','Utilisez la page Harbor approuvée pour soumettre les modifications.']
 ,['The selected company changed. Refresh and review this request in its original company.','所选公司已更改。请刷新并在原公司中检查此请求。','所選公司已變更。請重新整理，並在原公司中檢查此請求。','L’entreprise sélectionnée a changé. Actualisez et vérifiez cette demande dans son entreprise d’origine.']
 ,['The requested values are invalid. Refresh and review before trying again.','请求的值无效。请刷新并检查后再试。','請求的值無效。請重新整理並檢查後再試。','Les valeurs demandées sont invalides. Actualisez et vérifiez avant de réessayer.']
];
export const securityCatalogue=Object.fromEntries(rows.map(([key,sc,tc,fr])=>[key,{'zh-Hans':sc,'zh-Hant':tc,fr}]));

