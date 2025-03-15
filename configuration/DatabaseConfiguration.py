class  DatabaseConfiguration:

    app_jpa = "spring.jpa.hibernate.ddl-auto=none"
    app_hib_dial = "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect"
    app_hib_nmg = "spring.jpa.hibernate.naming.physical-strategy=org.hibernate.boot.model.naming.PhysicalNamingStrategyStandardImpl"
    app_hib_seq = "spring.jpa.hibernate.use-new-id-generator-mappings=false"
    # !!!! - when running on an EC2, we need '?enabledTLSProtocols=TLSv1.2' appended to the jdbc URL now
    app_mysql_conn = "spring.datasource.url=jdbc:mysql://locahost:3306/<schemaname>"
    app_mysql_usr = "spring.datasource.username=username"
    app_mysql_pwd = "spring.datasource.password=password"
    app_jpa_show = "spring.jpa.show-sql=true"