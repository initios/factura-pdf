from reportlab.platypus import NextPageTemplate, PageBreak
from facturapdf.helper import chunks


class DefaultStoryBuilder(object):
    def create(self, strategy, template, data):
        header = strategy.create_header(data)
        customer_section = strategy.create_customer_table(data)
        invoice_footer = strategy.create_invoice_footer(data)
        footer = strategy.create_footer(data)

        story = [
            NextPageTemplate(template.FIRST_PAGE_TEMPLATE_ID)
        ]

        rows_chunks = chunks(data.rows, strategy.MAX_ROWS_PER_TABLE, strategy.FILL_ROWS_WITH)

        for counter, row_chunk in enumerate(rows_chunks):
            is_first_page = counter == 0
            is_last_page = len(rows_chunks) == counter+1

            story.extend(header)
            story.extend(strategy.create_metadata_table(counter + 1, len(rows_chunks), data))

            if is_first_page:
                story.extend(customer_section)

            story.append(
                strategy.create_rows_table(row_chunk, data, is_last_page))

            if is_last_page:
                story.extend(invoice_footer)

            story.extend(footer)
            story.append(NextPageTemplate(template.LATER_PAGES_TEMPLATE_ID))

            if not is_last_page:
                story.append(PageBreak())

        return story