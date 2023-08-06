import argparse
import sys
import re



subnames = {'prod': ['prod', 'prd', 'production', 'prod-dev', 'prod-admin'],
            'stage': ['stage', 'stg', 'staging', 'stag', 'stag-dev', 'stag-admin'],
            'dev': ['dev', 'develop', 'developer', 'developing', 'dev-admin', 'dev-stage'],
            'admin': ['admin', 'adm', 'administrating'],
            'internal': ['internal', 'local', 'localhost', 'local-host'],
            'test': ['test', 'testing', 'test-dev', 'test-stage', 'test-admin']}



def make_mutation(domain, full_match):

    domain, tld = '.'.join(domain.split('.')[:-1]), domain.split('.')[-1]

    mutations = []

    is_found = False
    found_category = None
    found_value = None

    for category, values in subnames.items():
        for value in values:
            if full_match:
                if re.search(rf'\b{value}\b', domain):
                    is_found = True
                    found_category = category
                    found_value = value
                    break

            else:
                if value in domain:
                    is_found = True
                    found_category = category
                    found_value = value
                    break

            if is_found:
                break

    if is_found:
        subnames_for_replace = []
            
        for category, values in subnames.items():
            if category != found_category:
                subnames_for_replace.extend(values)
            
        for subname in subnames_for_replace:
                
            if full_match:
                new_domain = re.sub(rf'\b{found_value}\b', subname, domain)
            else:
                new_domain = domain.replace(found_value, subname)

            mutations.append(f'{new_domain}.{tld}')

    return mutations



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Subdomain mutations with popular keywords')
    parser.add_argument('-i', '--input', nargs='?',  type=argparse.FileType('r'), default=sys.stdin, help='input file with subdomains')
    parser.add_argument('-f', '--full-match', dest='full_match', default=False, required=False, action='store_true', help='replace only full words')
    parser.add_argument('-u', '--unique', dest='unique_only', default=True, required=False, action='store_true', help='save only unique subdomains')
    parser.set_defaults(full_match=False)
    parser.set_defaults(unique_only=True)
    args = parser.parse_args()

    try:
        domains = [line.strip() for line in args.input.readlines()]
    except Exception as e:
        print(e)
        sys.exit()

    total_mutations = []

    for domain in domains:
        mutations = make_mutation(domain, args.full_match)
        total_mutations.extend(mutations)

    total_mutations = list(set(total_mutations))

    if args.unique_only:
        unique_mutations = []
        
        for mutation in total_mutations:
            if mutation not in domains:
                unique_mutations.append(mutation)

        total_mutations = unique_mutations

    for mutation in total_mutations:
        print(mutation)