<html>
 <head>
  <title>Task 2</title>
 </head>
 <body>
   <form method="post">
     <p><b>Введите e-mail:</b><br>
     <input type="text" name="email">
    </p>
    <input type="submit" name="test" id="test" value="RUN" /><br/>
   </form>
   <?php
   if(array_key_exists('test',$_POST)){
      testfun();
   }
   function testfun()
   {
      $name = $_POST["email"];
      echo nl2br("$name\n");
      $dbconn = pg_connect("host=127.0.0.1 port=5432 dbname=forlogs user=postgres password=12345") or die('Не удалось соединиться: '.pg_last_error());
      echo "Совпадения из таблицы log: ";
      $tbname = "log";
      $count = "SELECT COUNT(*) FROM log WHERE address = '$name'" or die('Не удалось соединиться: '.pg_last_error());
      $count = pg_query($count);
      $query = "SELECT created, str FROM log WHERE address = '$name' ORDER BY int_id";
      $arr = pg_fetch_array($count, null, PGSQL_NUM);
      $count = $arr[0];
      if($count != 0 && $count != 100){
      echo "$count\n";
      $result = pg_query($query) or die('Ошибка запроса: ' . pg_last_error());
      echo "<table>\n";
      $ch = 0;
      while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
        $ch++;
        if ($ch == 100) {
          echo nl2br("запрос превышает 100 строк\n");
          break;
        }
        echo "\t<tr>\n";
        foreach ($line as $col_value) {
          echo "\t\t<td>$col_value</td>\n";
        }
        echo "\t</tr>\n";
      }
      echo "</table>\n";
    }
    if ($count == 0) {
      echo nl2br("совпадений не найдено\n");
    }
      echo "Совпадения из таблицы message:\n";
      $tbname = "message";
      $count = "SELECT COUNT(*) FROM message WHERE str LIKE '${name}%'" or die('Не удалось соединиться: '.pg_last_error());
      $count = pg_query($count);
      $query = "SELECT created, str FROM message WHERE str LIKE '${name}%' ORDER BY int_id";
      $arr = pg_fetch_array($count, null, PGSQL_NUM);
      $count = $arr[0];
      if($count != 0 && $count != 100){
      echo "$count\n";
      $result = pg_query($query) or die('Ошибка запроса: ' . pg_last_error());
      echo "<table>\n";
      $ch = 0;
      while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
        $ch++;
        if ($ch == 100) {
          echo nl2br("запрос превышает 100 строк\n");
          break;
        }
        echo "\t<tr>\n";
        foreach ($line as $col_value) {
          echo "\t\t<td>$col_value</td>\n";
        }
        echo "\t</tr>\n";
      }
      echo "</table>\n";
    }
    if ($count == 0) {
      echo nl2br("совпадений не найдено\n");
    }
  }
   ?>
 </body>
</html>
