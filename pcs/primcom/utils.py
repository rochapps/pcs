import csv

from .models import TraitData


class Average(object):
    def __init__(self, items=None):
        self.items = items or []

    def push(self, value):
        self.items.append(value)

    def reset(self):
        self.items = []

    def get_avg(self):
        if len(self.items):
            return sum(self.items) / len(self.items)
        return 0


class Aggregator(object):
    def __init__(self, items=None, taxonomy=None, traits=None, item=None, ops=None):
        self.items = items or {}
        self.taxonomy = taxonomy
        self.traits = traits
        self.item = item
        self.ops = ops

    def push(self, key, value):
        self.item = value
        traits = self.items.get(key, [])
        traits.append(value)
        self.items[key] = traits

    def reset(self):
        self.items = {}

    def get_avg(self, key, trait_type, sex):
        avg = Average()
        for item in self.items.get(key, []):
            if item.trait_type == trait_type and item.sex == sex:
                avg.push(item.trait_value)
        return avg.get_avg()

    def get_row(self, sex):
        item = self.item
        row = [
            item.taxonomy.species_name(self.taxonomy),
            item.taxonomy.species_reported_name,
            sex or 'unknown',
        ]
        for trait_id, trait in self.traits.items():
            for op in self.ops:
                avg = self.get_avg(trait_id, op, sex)
                row.append(avg)
        return row


def write_raw_data_file(response, qs, traits, taxonomy):
    writer = csv.writer(response)
    writer.writerow(TraitData.get_csv_headers())
    for record in qs:
        writer.writerow(record.get_csv_data(species_taxonomy=taxonomy))


def write_mean_data_file(response, qs, traits, taxonomy):
    writer = csv.writer(response)
    ops = [TraitData.MEAN]
    headers = [
        'species_name',
        'species_reported_name',
        'sex',
    ]
    for key, trait in traits.items():
        for op in ops:
            headers.append("{0} ({1})".format(trait.name, op))
    writer.writerow(headers)
    aggregator = Aggregator(taxonomy=taxonomy, traits=traits, ops=ops)
    first_record = qs[0]
    species_reported_name = first_record.taxonomy.species_reported_name
    for record in qs:
        if record.taxonomy.species_reported_name == species_reported_name:
            aggregator.push(record.trait.id, record)
        else:
            if aggregator.items:
                # species name or trait has changed but we have records ready to be written
                male_row = aggregator.get_row('m')
                female_row = aggregator.get_row('f')
                none_row = aggregator.get_row('')
                writer.writerow(male_row)
                writer.writerow(female_row)
                writer.writerow(none_row)
                # reset aggregator so that the new specie can be added
                aggregator.reset()
            species_reported_name = record.taxonomy.species_reported_name
            aggregator.push(record.trait.id, record)
