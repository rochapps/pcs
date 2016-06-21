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

    def get_avg(self, key, trait_type):
        avg = Average()
        for item in self.items.get(key, []):
            if item.trait_type == trait_type:
                avg.push(item.trait_value)
        return avg.get_avg() or 'NA'

    def get_row(self):
        item = self.item
        row = [
            item.taxonomy.species_name(self.taxonomy),
        ]
        for trait_id, trait in self.traits.items():
            for op in self.ops:
                avg = self.get_avg(trait_id, op)
                row.append(avg)
        return row


def write_raw_data_file(file_name, qs, traits, taxonomy):
    with open(file_name, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(TraitData.get_csv_headers())
        for record in qs:
            writer.writerow(record.get_csv_data(species_taxonomy=taxonomy))


def write_mean_data_file(file_name, qs, traits, taxonomy):
    with open(file_name, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        ops = [TraitData.MEAN]
        headers = [
            'Species Name',
        ]
        for key, trait in traits.items():
            for op in ops:
                headers.append("{0} ({1})".format(trait.name, op))
        writer.writerow(headers)
        aggregator = Aggregator(taxonomy=taxonomy, traits=traits, ops=ops)
        first_record = qs[0]
        species_corrected_name = first_record.taxonomy.species_name(taxonomy)
        for record in qs:
            if record.taxonomy.species_name(taxonomy) == species_corrected_name:
                aggregator.push(record.trait.id, record)
            else:
                if aggregator.items:
                    row = aggregator.get_row()
                    writer.writerow(row)
                    aggregator.reset()
                species_corrected_name = record.taxonomy.species_name(taxonomy)
                aggregator.push(record.trait.id, record)


def write_location_data_file(file_name, qs):
    with open(file_name, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        headers = [
            'Site Name',
            'Park Reserve Name',
            'Nation',
            'Latitude',
            'Longitude',
            'Notes'
        ]
        writer.writerow(headers)
        for location in qs:
            notes = location.notes.encode('utf-8') if location.notes else ''
            writer.writerow([
                location.site_name.encode('utf-8'),
                location.park_reserve_name.encode('utf-8'),
                location.nation.encode('utf-8'),
                location.latitude,
                location.longitude,
                notes
            ])


def write_location_references_file(file_name, qs):
    with open(file_name, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        headers = [
            'Citation',
            'Full Reference',
            'Notes',
        ]
        writer.writerow(headers)
        for reference in qs:
            notes = reference.notes.encode('utf-8') if reference.notes else ''
            writer.writerow([
                reference.citation.encode('utf-8'),
                reference.full_reference.encode('utf-8'),
                notes,
            ])
