def add_key_hash(data, column_name: str, columns: list):
    """Adds a hashed key column based on the contents of the specified columns."""
    column_str = ','.join(columns)
    return data.selectExpr(f"md5(concat_ws(':', {column_str})) as {column_name}", "*")

def delta_overwrite(data, table: str) -> None:
    data.write.format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .saveAsTable(table)

def delta_upsert(data, table: str) -> None:
    col_list = data.columns
    update_stmt = ""
    insert_stmt_1 = ""
    insert_stmt_2 = ""

    # soft delete feature
    # run_soft_del = delta_soft_delete(data, table)

    # create merge stmt
    for i, col in enumerate(col_list):
        update_stmt += f"a.{col} = b.{col},\n"
        insert_stmt_1 += f"'{col}',\n"
        insert_stmt_2 += f"b.{col},\n"
        if i == len(col_list) - 1:
            update_stmt = update_stmt.strip(',\n')
            insert_stmt_1 = insert_stmt_1.strip(',\n')
            insert_stmt_2 = insert_stmt_2.strip(',\n')

    # write table
    data.createOrReplaceTempView("temp_table")
    merge_stmt = f"""
    MERGE INTO {table} a USING temp_table b
    ON a._keyhash = b._keyhash
    WHEN MATCHED THEN UPDATE SET {update_stmt}
    WHEN NOT MATCHED THEN INSERT ({insert_stmt_1}) VALUES ({insert_stmt_2})
    """
    # data.write.mode("upsert").insertInto(table)
    # print(merge_stmt)
    run_upsert = spark.sql(merge_stmt)
    return (None)