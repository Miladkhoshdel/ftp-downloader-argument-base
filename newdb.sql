CREATE TABLE "config" ("ftpserver" TEXT, "ftpuser" TEXT, "ftppass" TEXT, "filename" TEXT, "cwd" TEXT);
CREATE TABLE "informations" ("webserver" TEXT, "databaseserver" TEXT, "ftpserver" TEXT check(typeof("ftpserver") = 'text') , "ipaddress" TEXT check(typeof("ipaddress") = 'text') );
