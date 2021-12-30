from django.db.models import When, Case, QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.
from elasticsearch import Elasticsearch

from products.models import Product


def product_list(request: HttpRequest):
    search_keyword = request.GET.get("search_keyword", "")

    elasticsearch = Elasticsearch("http://192.168.56.101:9200", http_auth=("elastic", "elasticpassword"))
    ela_query_result = elasticsearch.sql.query(body={
        "query": f"""
        SELECT id
        FROM ela___products_product___v1
        WHERE MATCH(display_name, '{search_keyword}') OR MATCH(name, '{search_keyword}')
        ORDER BY score() DESC
        """
    })

    print(ela_query_result)

    ids = [row[0] for row in ela_query_result['rows']]

    order = Case(*[When(id=id, then=pos) for pos, id in enumerate(ids)])
    qs: QuerySet = Product.objects.filter(id__in=ids).order_by(order)

    product_dict_list = [{"id": product.id, "name": product.name, "display_name": product.display_name} for product in
                         qs]

    return HttpResponse(product_dict_list)
