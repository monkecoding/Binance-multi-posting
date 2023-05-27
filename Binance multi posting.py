from decimal import ROUND_HALF_UP, Decimal
import random

# Предполагается, что у вас уже есть необходимые ключи для работы с API Binance для создания и получения ордеров

def create_orders_on_binance(data):
    volume = data['volume']
    number = data['number']
    amount_dif = data['amountDif']
    side = data['side']
    symbol = data['symbol']
    type= data['type']
    price_min = data['priceMin']
    price_max = data['priceMax']
    
    orders = []
    remaining_volume = volume

    for i in range(number):
        if remaining_volume <= 0:
            break
        
        if i == number - 1: 
            order_volume = remaining_volume
        else: 
            order_volume = random.uniform(volume/number - amount_dif, volume/number + amount_dif)
        
        order_price = random.uniform(price_min, price_max)

        orders.append({
            'volume': Decimal(order_volume).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            'price': Decimal(order_price).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            'side': side,
            'symbol': symbol,
            'type': type,
        })
        
        remaining_volume -= order_volume
    
    return orders


# Примеры тестов

def test_create_orders_on_binance():
    data = {
        "symbol": 'BNBBTC',
        "volume": 10000.0,
        "number": 5,
        "amountDif": 50.0,
        "side": "SIDE_SELL",
        "type": "ORDER_TYPE_LIMIT",
        "priceMin": 200.0,
        "priceMax": 300.0
    } # Исходные данные скорректированы для большей схожести с данными необходимыми Binance
    
    orders = create_orders_on_binance(data)
    
    total_order_volume = sum(order['volume'] for order in orders).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP) # Проверяем общую сумму ордеров
    assert total_order_volume == 10000.0, "Несоответствие итоговой стоимости"  # Проверяем, что сумма объемов ордеров равна заданному объему
    assert len(orders) == 5, "Несоответствие количества ордеров"  # Проверяем, что создано 5 ордеров
    print(orders)
    print(total_order_volume)
    for order in orders:
        assert data['priceMin'] <= order['price'] <= data['priceMax'], "Несоотвествие цены"  # Проверяем, что цена каждого ордера находится в заданном диапазоне
        assert data['side'] == order['side'], "Несоотвествие ордера"  # Проверяем, что сторона каждого ордера соответствует заданной
        assert data['symbol'] == order['symbol'], "Несоотвествия единиц"  # Проверяем, что единицы каждого ордера соответствует заданным
        assert data['type'] == order['type'], "Несоотвествие типа"  # Проверяем, что тип каждого ордера соответствует заданному


test_create_orders_on_binance()