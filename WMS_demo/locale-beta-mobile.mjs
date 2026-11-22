const rows=[
 ['A saved request needs review in its original company before another change can be saved.','保存其他更改前，请先在原公司核查已保存的请求。','儲存其他變更前，請先在原公司核查已儲存的請求。','Vérifiez la demande enregistrée dans son entreprise d’origine avant d’enregistrer une autre modification.'],
 ['Company','公司','公司','Entreprise'],
 ['Open desktop / choose company','打开桌面版 / 选择公司','開啟桌面版 / 選擇公司','Ouvrir le bureau / choisir une entreprise'],
 ['A backup or restore is unconfirmed. Resolve it in Cloud backups before scanning.','备份或还原尚未确认。请先在云端备份中处理，再进行扫码。','備份或還原尚未確認。請先在雲端備份中處理，再進行掃碼。','Une sauvegarde ou restauration reste non confirmée. Résolvez-la dans les sauvegardes cloud avant de scanner.'],
 ['The saved scan has no matching company identity. Review it in its original company before continuing.','已保存扫码缺少匹配的公司信息。请先返回原公司核查该记录，再继续操作。','已儲存掃碼缺少相符的公司資訊。請先返回原公司核查該記錄，再繼續操作。','La lecture enregistrée ne correspond à aucune entreprise identifiée. Vérifiez-la dans son entreprise d’origine avant de continuer.'],
 ['Cloud beta warehouse','云端测试仓库','雲端測試倉庫','Entrepôt bêta cloud'],
 ['Cloud scanning is enabled for your role.','您的角色可使用云端扫码保存。','您的角色可使用雲端掃碼儲存。','La lecture cloud est activée pour votre rôle.'],
 ['This workspace is read-only. Stock lookup is available.','此工作区为只读，仍可查询库存。','此工作區為唯讀，仍可查詢庫存。','Cet espace est en lecture seule. La consultation du stock reste disponible.'],
 ['Pending scan recovery','待确认扫码恢复','待確認掃碼復原','Récupération de lecture non confirmée'],
 ['An earlier scan is unconfirmed. Review the saved record or retry the original scan.','先前扫码尚未确认。请核查已保存记录，或重试原始扫码。','先前掃碼尚未確認。請核查已儲存記錄，或重試原始掃碼。','Une lecture précédente reste non confirmée. Examinez le dossier ou réessayez la lecture initiale.'],
 ['Retry original scan','重试原始扫码','重試原始掃碼','Réessayer la lecture initiale'],
 ['Refresh warehouse','刷新仓库','重新整理倉庫','Actualiser l’entrepôt'],
 ['Review and retry the original unconfirmed scan?','已核查并重试原始未确认扫码？','已核查並重試原始未確認掃碼？','Après vérification, réessayer la lecture initiale non confirmée ?'],
 ['Cloud scanning is unavailable for your role.','您的角色不能保存云端扫码。','您的角色無法儲存雲端掃碼。','Votre rôle ne permet pas d’enregistrer des lectures cloud.'],
 ['No unconfirmed scan is waiting.','没有待确认的扫码。','沒有待確認的掃碼。','Aucune lecture non confirmée en attente.'],
 ['Original scan confirmed. Warehouse refreshed.','原始扫码已确认，仓库已刷新。','原始掃碼已確認，倉庫已重新整理。','Lecture initiale confirmée. Entrepôt actualisé.'],
 ['Refresh the workspace before saving.','保存前请刷新工作区。','儲存前請重新整理工作區。','Actualisez l’espace avant d’enregistrer.'],
 ['Save confirmed. Refresh the workspace before continuing.','已确认保存。继续前请刷新工作区。','已確認儲存。繼續前請重新整理工作區。','Enregistrement confirmé. Actualisez l’espace avant de continuer.'],
 ['Wait for the current save to finish.','请等待当前保存完成。','請等待目前儲存完成。','Attendez la fin de l’enregistrement.']
];
export const betaMobileCatalogue=Object.fromEntries(rows.map(([key,sc,tc,fr])=>[key,{'zh-Hans':sc,'zh-Hant':tc,fr}]));

