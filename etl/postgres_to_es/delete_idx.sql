DO
$$
DECLARE
    index_rec RECORD;
BEGIN
    -- Получаем информацию обо всех индексах в базе данных
    FOR index_rec IN (SELECT indexname, tablename FROM pg_indexes WHERE schemaname = 'content')
    LOOP
        -- Формируем команду DROP INDEX и выполняем ее
        EXECUTE format('DROP INDEX IF EXISTS %I.%I;', index_rec.tablename, index_rec.indexname);
    END LOOP;
END
$$;
