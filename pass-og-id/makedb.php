<?php
$dager = $_GET['dager'];
$date = date('Y-m-d');
// PASS
// ID-KORT
# PublicId = '8e859bd4c1752249665bf2363ea231e1678dbb7fc4decff862d9d41975a9a95a';
$PublicId = 'd1b043c75655a6756852ba9892255243c08688a071e3b58b64c892524f58d098';

$begynn_link = "https://pass-og-id.politiet.no/qmaticwebbooking/rest/schedule/branches/";
$slutt_link =";service" . "PublicId=" . $PublicId . ";customSlotLength=10";
$avdeling = $_GET['avdeling'];
$distrikt = false;
$id = false;
$db = new SQLite3('itWorks.db');
$db->exec("CREATE TABLE distrikt(id INTEGER PRIMARY KEY, distrikt_id TEXT,  distrikt_navn TEXT)");
$db->exec("CREATE TABLE avdeling(id INTEGER PRIMARY KEY, distrikt_id TEXT, distrikt_navn TEXT,  avdeling_navn TEXT, avdeling_id TEXT)");
$data = file_get_contents('https://pass-og-id.politiet.no/qmaticwebbooking/rest/schedule/branchGroups;servicePublicId=d1b043c75655a6756852ba9892255243c08688a071e3b58b64c892524f58d098');
$decoded_json = json_decode($data, true);
foreach ($decoded_json as $branch) {
    $distrikt_navn = $branch['name'];
    $distrikt_id = $branch['id'];
    $db->exec("INSERT INTO distrikt(distrikt_id, distrikt_navn) VALUES('$distrikt_id', '$distrikt_navn')");
    foreach ($branch['branches'] as $avd) {
        $avdeling_navn = $avd['name'];
        $avdeling_id = $avd['id'];
        $db->exec("INSERT INTO avdeling(distrikt_id, distrikt_navn, avdeling_navn, avdeling_id) VALUES('$distrikt_id', '$distrikt_navn', '$avdeling_navn', '$avdeling_id')");
    }
}
?>