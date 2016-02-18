function read(ele, id, mid) {
    target = document.getElementById(mid);
    alert("きた１")

    if (!ele.files.length) return; // ファイル未選択

    var file = ele.files[0];
    var fr = new FileReader();
    fr.readAsText(file); // ファイルをテキストとして読み込む

    fr.onload = function() {
        if (!isJson(fr.result)) {
            alert("きた２")
            target.innerHTML = "NG Json format."; // 判定結果を結果をerror_mesに
            return;
        }

        document.getElementById(id).value = fr.result; // 読み込み結果をtextareaに
        target.innerHTML = "OK Json format."; // 読み込み結果をerror_mesに
    };
    fr.readAsText(file); // ファイルをテキストとして読み込む
};

function json_check(id, mid) {
    target = document.getElementById(mid);

    if (isJson(document.getElementById(id).value)) {
        target.innerHTML = "OK Json format."; // 読み込み結果をerror_mesに
    } else {
        target.innerHTML = "NG Json format"; // 判定結果を結果をerror_mesに
    }

    return;
};

var isJson = function(arg) {
    alert(typeof(arg))
    arg = (typeof(arg) == "function") ? arg() : arg;
    if (typeof(arg) != "string") {
        return false;
    }
    try {
        arg = (!JSON) ? eval("(" + arg + ")") : JSON.parse(arg);
        return true;
    } catch (e) {
        return false;
    }
};

function json_check2() {

    target = document.getElementById("temp_output");

    if (isJson(document.getElementById('template_parameters').value)) {
        alert("きた6")
        target.innerHTML = "きた"; // 読み込み結果をerror_mesに
    } else {
        alert("きてない7")
        target.innerHTML = "きてない not"; // 判定結果を結果をerror_mesに
    }
    alert("おわり8")

    return;
}
