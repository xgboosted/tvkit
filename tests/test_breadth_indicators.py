"""
Tests for breadth indicator support in tvkit.

Tests the new functionality for INDEX-NDTH, INDEX-NDFI, INDEX-NDTW symbols.
"""

import pytest
from unittest.mock import AsyncMock, patch

from tvkit.api.utils import validate_symbols
from tvkit.helpers import validate_symbol_format, SymbolValidationError


class TestBreadthIndicatorValidation:
    """Test cases for breadth indicator symbol validation."""

    def test_validate_symbol_format_breadth_indicators(self) -> None:
        """Test that breadth indicators pass symbol format validation."""
        breadth_indicators = ['INDEX-NDTH', 'INDEX-NDFI', 'INDEX-NDTW']
        
        for symbol in breadth_indicators:
            # Should not raise an exception
            result = validate_symbol_format(symbol)
            assert result is True

    def test_validate_symbol_format_normal_symbols(self) -> None:
        """Test that normal symbols still work."""
        normal_symbols = ['NASDAQ:AAPL', 'BINANCE:BTCUSDT', 'NYSE:MSFT']
        
        for symbol in normal_symbols:
            result = validate_symbol_format(symbol)
            assert result is True

    def test_validate_symbol_format_invalid_symbols(self) -> None:
        """Test that invalid symbols are still rejected."""
        invalid_symbols = ['INVALID', 'INDEX-INVALID', 'NO:COLON:EXTRA']
        
        for symbol in invalid_symbols:
            with pytest.raises(SymbolValidationError):
                validate_symbol_format(symbol)

    @pytest.mark.asyncio
    async def test_validate_symbols_breadth_indicators(self) -> None:
        """Test that breadth indicators pass async symbol validation."""
        breadth_indicators = ['INDEX-NDTH', 'INDEX-NDFI', 'INDEX-NDTW']
        
        # Should not make HTTP requests for breadth indicators
        with patch('httpx.AsyncClient') as mock_client:
            for symbol in breadth_indicators:
                result = await validate_symbols(symbol)
                assert result is True
                
            # Verify no HTTP client was used (breadth indicators skip validation)
            mock_client.assert_not_called()

    @pytest.mark.asyncio
    async def test_validate_symbols_mixed_list(self) -> None:
        """Test validation with mixed list of normal and breadth indicator symbols."""
        mixed_symbols = ['INDEX-NDTH', 'NASDAQ:AAPL', 'INDEX-NDFI']
        
        # Mock HTTP client for normal symbols
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.raise_for_status.return_value = None
            mock_context = AsyncMock()
            mock_context.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_context
            
            result = await validate_symbols(mixed_symbols)
            assert result is True
            
            # Should be called once for the context manager
            mock_client.assert_called_once()

    @pytest.mark.asyncio
    async def test_validate_symbols_single_breadth_indicator(self) -> None:
        """Test validation with single breadth indicator."""
        result = await validate_symbols('INDEX-NDTH')
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_symbols_list_breadth_indicators(self) -> None:
        """Test validation with list of breadth indicators."""
        indicators = ['INDEX-NDTH', 'INDEX-NDFI', 'INDEX-NDTW']
        result = await validate_symbols(indicators)
        assert result is True

    def test_breadth_indicator_examples_in_error_message(self) -> None:
        """Test that breadth indicators appear in error message suggestions."""
        with pytest.raises(SymbolValidationError) as exc_info:
            validate_symbol_format('INVALID')
            
        error_message = str(exc_info.value)
        assert 'INDEX-NDTH' in error_message
        assert 'INDEX-NDFI' in error_message 
        assert 'INDEX-NDTW' in error_message


class TestBreadthIndicatorConstants:
    """Test the breadth indicator constants and their meanings."""
    
    def test_breadth_indicator_documentation(self) -> None:
        """Test that we document what each breadth indicator means."""
        # These should be the supported indicators from the issue description
        expected_indicators = {
            'INDEX-NDTH': 'Nasdaq 100 Stocks Above 200-Day Average',
            'INDEX-NDFI': 'Nasdaq 100 Stocks Above 50-Day Average', 
            'INDEX-NDTW': 'Nasdaq 100 Stocks Above 20-Day Average',
        }
        
        # All these should pass validation
        for symbol, description in expected_indicators.items():
            result = validate_symbol_format(symbol)
            assert result is True, f"Failed to validate {symbol}: {description}"