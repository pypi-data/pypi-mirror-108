import psycopg2
import pandas as pd


DB_HOST = 'localhost'
DB_NAME = 'Sheba_dump_full'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_PORT = '54320'
QUERY = '''select
           s.offering_id, sc.created_at::date as "sc_created", sc.status as "sc_status", sc.type, sc.female_sample_id, sc.male_sample_id,
           s.id, s.gender, s.is_urgent, s.pregnancy_sampling_week, s.sample_date,
           s.sample_number, s.state_type, s.urgency_reason, s.send_to_lab_date,
           r.id as "result id", r.sample_id, r.result_status, r.display_label,
           mi.clinical_significance,
           mut.primary_full_name, mut.primary_variant_name, mut.alt, mut.primary_pname, mut.ref, mut.hg38_start,
           pp.panel_type,
           g.name, g.chromosome,
           (select transfer_from from genetic_findings_comments gfc
            where gfc.results_id = r.id order by created_at limit 1) as "transfer_from",
           (select array_agg(transfer_to) from genetic_findings_comments gfc1 where gfc1.results_id = r.id group by results_id) as "transfer to",
           (select array_agg(comment) from genetic_findings_comments gfc1 where gfc1.results_id = r.id group by results_id) as "comment",
           (select text from translations join main_population_translations mpt on translations.id = mpt.translation_id
            where language_code='en' and mpt.population_id=pt.paternal_grand_mother_ethnicity_id) as "Paternal Gradma",
           (select text from translations join main_population_translations mpt on translations.id = mpt.translation_id
            where language_code='en' and mpt.population_id=pt.paternal_grand_father_ethnicity_id) as "Paternal Gradpa",
           (select text from translations join main_population_translations mpt on translations.id = mpt.translation_id
            where language_code='en' and mpt.population_id=pt.maternal_grand_mother_ethnicity_id) as "Maternal Gradma",
           (select text from translations join main_population_translations mpt on translations.id = mpt.translation_id
            where language_code='en' and mpt.population_id=pt.maternal_grand_father_ethnicity_id) as "Maternal Gradpa",
           (select created_at::date as "LAB report date" from pdf_reports
            where sample_card_id=sc.id and report_type='LAB' and active=true order by created_at DESC limit 1) as "Lab report date",
           (select created_at::date as "LAB report date" from pdf_reports
            where sample_card_id=sc.id and report_type='GC' and active=true order by created_at DESC limit 1) as "GC report date"
    from sample_card sc
    left join samples s on sc.female_sample_id = s.id or sc.male_sample_id= s.id
    --left join samples s on sc.male_sample_id= s.id
    left join patients pt on s.patient_id = pt.id
    left join results r on s.id = r.sample_id
    left join results_mutations rm on r.id = rm.result_id
    left join mutations_infos mi on rm.mutation_info_id = mi.id
    left join mutations mut on mi.mutation_id = mut.id
    left join genes g on mut.gene_id = g.id
    left join
        (select * from offering_panels op
            left join panels p on op.panel_id = p.id
            left join panel_mutations pm on p.id = pm.panel_id
            ) pp
            on mut.id=pp.mutation_id
    where
          sc.status = 'GC_REPORTED'
          and sc.type <> 'HIDDEN'
          --and sc.type = 'COUPLE'
          and  (pp.name is null or pp.name not like '%FMF%')
          and (s.offering_id=pp.offering_id or pp.offering_id is null)
        --and sample_id=1565
    order by sc.female_sample_id;'''
COLNAMES = ['offering_id', 'sc_created', 'sc_status', 'type', 'female_sample_id', 'male_sample_id', 'id',
                'gender', 'is_urgent', 'pregnancy_sampling_week', 'sample_date', 'sample_number', 'state_type',
                'urgency_reason', 'send_to_lab_date', 'result_id', 'sample_id', 'result_status',
                'display_label', 'clinical_significance', 'primary_full_name', 'primary_variant_name', 'alt',
                'primary_pname', 'ref', 'hg38_start','panel_type', 'name', 'chromosome', 'transfer_from', 'transfer_to',
                'comment', 'paternal_gradma', 'paternal_gradpa', 'maternal_gradma', 'matrnal_gradpa', 'lab_report_date'
                , 'gc_report_date']


class DBConnection:
    def __init__(self):
        self.host = DB_HOST
        self.name = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.port = DB_PORT
        self.conn = None

    def connect(self):
        """
        Connect to postgres server
        :param self
        :return: self.conn
        """
        if self.conn is None:
            print('Connecting to the PostgreSQL database...')
            try:
                self.conn = psycopg2.connect(host=self.host,
                                             dbname=self.name,
                                             user=self.user,
                                             password=self.password,
                                             port=self.port)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                # sys.exit(1)
            print("Connection successful")
        return self.conn


class SQLtodf:
    def __init__(self, conn_param):
        self.select_query = QUERY
        self.col_names = COLNAMES
        self.cursor = conn_param.cursor()

    def sql_to_df(self):
        """
        Convert postgres database to pandas dataframe
        :param self
        :return: df:pd.DataFrame
        """
        try:
            self.cursor.execute(self.select_query)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.cursor.close()
            return 1

        # Naturally we get a list of tupples
        tupples = self.cursor.fetchall()
        self.cursor.close()

        # We just need to turn it into a pandas dataframe
        df = pd.DataFrame(tupples, columns=self.col_names)

        return df




